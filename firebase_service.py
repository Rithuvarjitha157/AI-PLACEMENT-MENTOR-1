"""
AI Service Layer.

Provides a single call_llm() function that abstracts over:
  - OpenAI API
  - Anthropic (Claude) API
  - Mock mode (no API key required — returns realistic canned JSON)

Controlled via LLM_PROVIDER env var: "openai" | "anthropic" | "mock"
This lets the whole app run and demo perfectly even with zero API keys.
"""
import os
import json
import requests

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


def _call_openai(prompt: str, system: str = None) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    body = {"model": OPENAI_MODEL, "messages": messages, "temperature": 0.4}
    resp = requests.post(url, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _call_anthropic(prompt: str, system: str = None) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    body = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        body["system"] = system
    resp = requests.post(url, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    content = resp.json()["content"]
    return "".join(block.get("text", "") for block in content)


def call_llm(prompt: str, system: str = None, mock_response: str = "{}") -> str:
    """
    Central entry point. Every feature module calls this.
    Falls back gracefully to mock_response if provider is "mock" or
    if the real API call fails for any reason (keeps demo alive).
    """
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        try:
            return _call_openai(prompt, system)
        except Exception as e:
            print(f"[ai_service] OpenAI call failed, falling back to mock: {e}")
            return mock_response
    elif LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
        try:
            return _call_anthropic(prompt, system)
        except Exception as e:
            print(f"[ai_service] Anthropic call failed, falling back to mock: {e}")
            return mock_response
    else:
        return mock_response


def safe_json_parse(raw_text: str, fallback: dict) -> dict:
    """Strips markdown fences if present and parses JSON safely."""
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
    try:
        return json.loads(cleaned)
    except Exception as e:
        print(f"[ai_service] JSON parse failed: {e}. Raw: {raw_text[:200]}")
        return fallback
