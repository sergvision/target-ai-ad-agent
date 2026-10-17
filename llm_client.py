"""LLM client for the Target AI Ad Agent."""

import os
from typing import Any

import requests


def generate_text(system_prompt: str, user_prompt: str) -> str:
    """Generate text using Gemini or OpenAI API."""

    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{model}:generateContent"
        )

        response = requests.post(
            url,
            params={"key": api_key},
            json={
                "system_instruction": {
                    "parts": [{"text": system_prompt}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": user_prompt}],
                    }
                ],
                "generationConfig": {"temperature": 0.4},
            },
            timeout=60,
        )

        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.4,
            },
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    raise ValueError("LLM_PROVIDER must be 'gemini' or 'openai'")
