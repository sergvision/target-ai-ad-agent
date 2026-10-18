
"""LLM client for the Target AI Ad Agent.

Supports Gemini and OpenAI through environment variables.
API keys must never be stored in source code.
"""

import os
from typing import Any

import requests


def generate_text(system_prompt: str, user_prompt: str) -> str:
    """Generate text using the configured LLM provider."""

    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()

    if provider == "gemini":
        return _generate_with_gemini(system_prompt, user_prompt)

    if provider == "openai":
        return _generate_with_openai(system_prompt, user_prompt)

    raise ValueError(
        "Unsupported LLM_PROVIDER. Use 'gemini' or 'openai'."
    )


def _generate_with_gemini(
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Call the Gemini generateContent API."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured in the environment."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent"
    )

    payload = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
        },
    }

    try:
        response = requests.post(
            url,
            params={"key": api_key},
            json=payload,
            timeout=60,
        )
    except requests.Timeout as exc:
        raise RuntimeError(
            "Gemini API request timed out after 60 seconds."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to Gemini API: {type(exc).__name__}."
        ) from exc

    if not response.ok:
        # Do not include the request URL or API key in error messages.
        error_detail = response.text[:500]
        raise RuntimeError(
            f"Gemini API returned HTTP {response.status_code}: "
            f"{error_detail}"
        )

    try:
        data: dict[str, Any] = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "Gemini API returned an invalid JSON response."
        ) from exc

    candidates = data.get("candidates") or []
    if not candidates:
        feedback = data.get("promptFeedback", {})
        reason = feedback.get("blockReason", "No candidate returned")
        raise RuntimeError(f"Gemini produced no response: {reason}.")

    content = candidates[0].get("content", {})
    parts = content.get("parts", [])

    text_parts = [
        part["text"]
        for part in parts
        if isinstance(part, dict) and isinstance(part.get("text"), str)
    ]

    if not text_parts:
        finish_reason = candidates[0].get("finishReason", "unknown")
        raise RuntimeError(
            f"Gemini returned no text. Finish reason: {finish_reason}."
        )

    return "\n".join(text_parts).strip()


def _generate_with_openai(
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Call the OpenAI Chat Completions API."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured in the environment."
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.4,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=60,
        )
    except requests.Timeout as exc:
        raise RuntimeError(
            "OpenAI API request timed out after 60 seconds."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to OpenAI API: {type(exc).__name__}."
        ) from exc

    if not response.ok:
        error_detail = response.text[:500]
        raise RuntimeError(
            f"OpenAI API returned HTTP {response.status_code}: "
            f"{error_detail}"
        )

    try:
        data: dict[str, Any] = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "OpenAI API returned an invalid JSON response."
        ) from exc

    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("OpenAI API returned no completion choices.")

    message = choices[0].get("message", {})
    content = message.get("content")

    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("OpenAI API returned an empty text response.")

    return content.strip()
