"""
Gemini service for PromptWise.
Manages Google GenAI client, model fallbacks, error handling, and response generation.
"""

import json
import re
import time
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st
from google import genai
from google.genai import types

from prompts.templates import SYSTEM_PROMPT

# Models list matching project configuration
MODELS = [
    "gemini-3.5-flash-lite"
]


@st.cache_resource
def get_gemini_client() -> Optional[genai.Client]:
    """Initialize and cache the Gemini API client using Streamlit secrets."""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
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
    if "GEMINI_API_KEY" not in st.secrets:
        return (
            False,
            "GEMINI_API_KEY is missing from `.streamlit/secrets.toml`. "
            "Please add your key to enable AI generation.",
        )
    client = get_gemini_client()
    if not client:
        err = st.session_state.get("client_error", "Unknown error")
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

            errors.append(f"{model}: Returned empty response")

        except Exception as e:
            err_str = str(e)
            err_upper = err_str.upper()
            errors.append(f"{model}: {err_str}")

            # Recognize retryable conditions
            retryable = any(
                code in err_upper
                for code in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "502",
                    "504",
                    "DEADLINE_EXCEEDED",
                    "TIMEOUT",
                ]
            )

            if not retryable:
                # Fatal error (e.g. invalid key, bad request)
                raise RuntimeError(f"Gemini API error ({model}): {err_str}")

            time.sleep(1.5)

    # If all models failed
    all_err_msg = "\n".join(errors)
    if "429" in all_err_msg or "RESOURCE_EXHAUSTED" in all_err_msg:
        raise RuntimeError(
            "Gemini API quota exceeded (Rate limit / 429). Please wait a moment before trying again."
        )
    elif "503" in all_err_msg or "UNAVAILABLE" in all_err_msg:
        raise RuntimeError(
            "Gemini service is temporarily experiencing high demand (503). Please retry in a few moments."
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
    # Replace single backslash followed by non-standard escape character with just the character
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
