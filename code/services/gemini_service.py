"""
Gemini Service for PromptWise.
Manages Google GenAI client initialization, model fallbacks, retry handling,
and robust JSON/text response generation for an academic study assistant prototype.
"""

import json
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st
from google import genai
from google.genai import types

from prompts.templates import SYSTEM_PROMPT

# Verified models configured for generation with automatic fallback
# Primary: gemini-3.5-flash-lite (fast inference, high responsiveness)
# Secondary fallback: gemini-3.1-flash-lite (verified active and responsive)
MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
]


def resolve_api_key() -> Optional[str]:
    """Retrieve Gemini API key from Streamlit secrets or environment variables.

    Never prints, logs, or exposes the key.
    """
    key = None
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not key:
        key = os.environ.get("GEMINI_API_KEY")

    if key:
        key = key.strip().strip('"').strip("'")
    return key if key else None


@st.cache_resource
def get_gemini_client() -> Optional[genai.Client]:
    """Initialize and cache the Gemini API client using Streamlit secrets or environment variables.

    Handles missing credentials gracefully and never exposes secrets in logs.
    """
    try:
        api_key = resolve_api_key()
        if not api_key:
            return None
        return genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=45000),
        )
    except Exception as e:
        # Sanitize exception message so raw keys never leak
        err_msg = str(e)
        api_key = resolve_api_key()
        if api_key and api_key in err_msg:
            err_msg = err_msg.replace(api_key, "[REDACTED_API_KEY]")
        st.session_state["client_error"] = err_msg
        return None


def is_client_ready() -> Tuple[bool, str]:
    """Check if the Gemini client is configured and ready."""
    api_key = resolve_api_key()
    if not api_key:
        return (
            False,
            "GEMINI_API_KEY is not configured. Please add your key to `.streamlit/secrets.toml` "
            "or set the GEMINI_API_KEY environment variable.",
        )
    client = get_gemini_client()
    if not client:
        err = st.session_state.get("client_error", "Initialization failed")
        return False, f"Failed to initialize Gemini client: {err}"
    return True, "Client initialized successfully."


def get_api_status() -> Dict[str, Any]:
    """Get current API connection and generation status for UI display.

    Distinguishes between client initialization and successful API generation.
    Never shows 'API Connected' merely because a client object was created.
    """
    api_key = resolve_api_key()
    if not api_key:
        return {
            "status": "missing_credentials",
            "icon": "🔴",
            "color": "#ef4444",
            "label": "Credentials Missing",
            "details": "GEMINI_API_KEY not found in secrets or env",
            "model": None,
        }

    client = get_gemini_client()
    if not client:
        err = st.session_state.get("client_error", "Init failed")
        return {
            "status": "init_failed",
            "icon": "🔴",
            "color": "#ef4444",
            "label": "Client Init Failed",
            "details": err[:50],
            "model": None,
        }

    # Check session state for generation events
    api_status = st.session_state.get("api_status", "client_initialized")
    last_model = st.session_state.get("last_active_model", None)
    last_err = st.session_state.get("last_api_error", None)
    used_fallback = st.session_state.get("used_fallback", False)

    if api_status == "verified_active" and last_model:
        fallback_tag = " (Fallback)" if used_fallback else ""
        return {
            "status": "verified_active",
            "icon": "🟢",
            "color": "#10b981",
            "label": "API Active & Verified",
            "details": f"Active: {last_model}{fallback_tag}",
            "model": last_model,
        }
    elif api_status == "request_failed":
        return {
            "status": "request_failed",
            "icon": "🔴",
            "color": "#ef4444",
            "label": "API Request Failed",
            "details": (last_err or "Generation error")[:50],
            "model": None,
        }
    else:
        # Client initialized, but no live prompt has run yet
        return {
            "status": "client_initialized",
            "icon": "🟡",
            "color": "#f59e0b",
            "label": "Client Initialized",
            "details": f"Configured ({MODELS[0]}), awaiting request",
            "model": MODELS[0],
        }


def call_gemini(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    response_mime_type: Optional[str] = None,
    force_model: Optional[str] = None,
) -> str:
    """Execute a prompt against the configured Gemini models with retry and error handling.
    
    Args:
        prompt: The main user or task prompt.
        system_instruction: Optional system instruction overriding the default.
        temperature: Sampling temperature.
        response_mime_type: Optional MIME type (e.g., "application/json").
        force_model: Optional model ID override for testing fallback directly.

    Returns:
        Generated text response.
    """
    client = get_gemini_client()
    if not client:
        ready, msg = is_client_ready()
        st.session_state["api_status"] = "missing_credentials"
        st.session_state["last_api_error"] = msg
        raise RuntimeError(msg)

    sys_instr = system_instruction if system_instruction is not None else SYSTEM_PROMPT
    candidate_models = [force_model] if force_model else MODELS
    errors: List[str] = []

    for model in candidate_models:
        # Up to 2 attempts per model for transient drops (avoiding long delays in live demos)
        for attempt in range(2):
            try:
                config_kwargs = {
                    "system_instruction": sys_instr,
                    "temperature": temperature,
                }
                if response_mime_type:
                    config_kwargs["response_mime_type"] = response_mime_type

                config = types.GenerateContentConfig(**config_kwargs)

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config,
                )

                if response and response.text:
                    # Successfully generated
                    st.session_state["api_status"] = "verified_active"
                    st.session_state["last_active_model"] = model
                    st.session_state["used_fallback"] = (model != MODELS[0])
                    st.session_state["last_api_error"] = None
                    return response.text.strip()

                errors.append(f"{model} (attempt {attempt+1}): Empty response")

            except Exception as e:
                err_str = str(e)
                api_key = resolve_api_key()
                if api_key and api_key in err_str:
                    err_str = err_str.replace(api_key, "[REDACTED_API_KEY]")
                err_upper = err_str.upper()
                errors.append(f"{model} (attempt {attempt+1}): {err_str}")

                # Immediate fatal errors that should abort immediately (e.g., invalid API key, bad requests)
                is_auth_error = any(
                    token in err_upper
                    for token in [
                        "API_KEY_INVALID",
                        "API KEY NOT VALID",
                        "INVALID_API_KEY",
                        "PERMISSION_DENIED",
                        "INVALID_ARGUMENT",
                    ]
                )
                if is_auth_error:
                    st.session_state["api_status"] = "request_failed"
                    st.session_state["last_api_error"] = "Invalid or expired Gemini API key."
                    raise RuntimeError(
                        "Gemini API Authentication Error: Invalid or expired API key. "
                        "Please check your GEMINI_API_KEY in `.streamlit/secrets.toml` or environment variables."
                    )

                # Transient errors (quota 429, 500, 502, 503, 504, connection resets, timeouts)
                # Short exponential backoff to avoid long delays during live demos
                time.sleep(2.0 * (attempt + 1))

    # If all candidate models and retries failed
    st.session_state["api_status"] = "request_failed"
    all_err_msg = "\n".join(errors)
    st.session_state["last_api_error"] = "All configured models failed to generate content."

    if "429" in all_err_msg or "RESOURCE_EXHAUSTED" in all_err_msg:
        raise RuntimeError(
            "Gemini API rate limit exceeded (Quota 429). Please wait a few seconds and try again."
        )
    elif "503" in all_err_msg or "UNAVAILABLE" in all_err_msg:
        raise RuntimeError(
            "Gemini service is temporarily under high demand (503). Retrying shortly usually succeeds."
        )
    elif "8" in all_err_msg and "NODENAME" in all_err_msg:
        raise RuntimeError(
            "Network connection error: Unable to resolve Gemini API endpoint. Please check your internet connection."
        )
    else:
        raise RuntimeError(
            f"All configured models failed to generate content. Attempted models: {candidate_models}.\nDetails:\n{all_err_msg}"
        )


def clean_json_string(text: str) -> str:
    """Extract and sanitize JSON from model output that might include markdown fences."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    return text


def sanitize_escapes(text: str) -> str:
    """Sanitize invalid escape sequences like LaTeX symbols in JSON strings."""
    return re.sub(r'\\([^"\\/bfnrtu])', r'\1', text)


def parse_json_response(raw_text: str) -> Dict[str, Any]:
    """Parse JSON output safely, falling back to sanitization and bracket extraction."""
    cleaned = clean_json_string(raw_text)

    # Attempt 1: Direct parse
    try:
        return json.loads(cleaned, strict=False)
    except Exception:
        pass

    # Attempt 2: Sanitize invalid backslash escapes
    try:
        sanitized = sanitize_escapes(cleaned)
        return json.loads(sanitized, strict=False)
    except Exception:
        pass

    # Attempt 3: Extract outermost { ... }
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = cleaned[start : end + 1]
        try:
            return json.loads(snippet, strict=False)
        except Exception:
            try:
                return json.loads(sanitize_escapes(snippet), strict=False)
            except Exception:
                pass

    raise ValueError(
        f"Could not parse valid JSON from model response. Preview:\n{raw_text[:200]}"
    )
