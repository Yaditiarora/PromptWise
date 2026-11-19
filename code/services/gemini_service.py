"""
Gemini Service for PromptWise.
Manages Google GenAI client, model fallbacks, error handling, and robust response generation.
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

# Models configured for generation with automatic fallback
# Primary: gemini-3.5-flash-lite (fastest, highest quota responsiveness)
# Secondary fallback: gemini-3.8-flash
MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
]


def resolve_api_key() -> Optional[str]:
    """Retrieve Gemini API key from Streamlit secrets or environment variables."""
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
    return key


@st.cache_resource
def get_gemini_client() -> Optional[genai.Client]:
    """Initialize and cache the Gemini API client using Streamlit secrets or environment variables."""
    try:
        api_key = resolve_api_key()
        if not api_key:
            return None
        return genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=60000),
        )
    except Exception as e:
        st.session_state["client_error"] = str(e)
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


def call_gemini(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.7,
    response_mime_type: Optional[str] = None,
) -> str:
    """Execute a prompt against the configured Gemini models with retry and error handling.
    
    Args:
        prompt: The main user or task prompt.
        system_instruction: Optional system instruction overriding the default.
        temperature: Sampling temperature.
        response_mime_type: Optional MIME type (e.g., "application/json").

    Returns:
        Generated text response.
    """
    client = get_gemini_client()
    if not client:
        ready, msg = is_client_ready()
        raise RuntimeError(msg)

    sys_instr = system_instruction if system_instruction is not None else SYSTEM_PROMPT
    errors: List[str] = []

    for model in MODELS:
        for attempt in range(3):  # Up to 3 attempts with exponential backoff for transient spikes
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
                    return response.text.strip()

                errors.append(f"{model} (attempt {attempt+1}): Returned empty response")

            except Exception as e:
                err_str = str(e)
                err_upper = err_str.upper()
                errors.append(f"{model} (attempt {attempt+1}): {err_str}")

                # Immediate fatal errors that should abort immediately (e.g., bad API key)
                is_auth_error = any(
                    token in err_upper
                    for token in ["API_KEY_INVALID", "API KEY NOT VALID", "INVALID_API_KEY", "PERMISSION_DENIED"]
                )
                if is_auth_error:
                    raise RuntimeError(
                        f"Gemini API Authentication Error: Invalid or expired API key. "
                        f"Please check your GEMINI_API_KEY in `.streamlit/secrets.toml` or environment variables."
                    )

                # Transient errors (quota 429, 503, connection resets, timeouts, DNS/socket drops)
                time.sleep(2.0 * (attempt + 1))

    # If all candidate models failed
    all_err_msg = "\n".join(errors)
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
            f"All configured models failed to generate content. Details:\n{all_err_msg}"
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
