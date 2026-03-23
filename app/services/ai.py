import os

from openai import OpenAI


def generate_text(prompt: str) -> str:
    mock = os.getenv("MOCK_AI", "").lower() in ("1", "true", "yes")
    if mock:
        return f"[mock-ai] {prompt.strip()[:2000]}"

    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise ValueError("Set OPENAI_API_KEY or MOCK_AI=1 for local testing.")

    client = OpenAI(api_key=key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        choice = response.choices[0].message.content
        if choice is None:
            raise ValueError("Empty response from OpenAI")
        return choice.strip()
    except Exception:
        # Development fallback: keep /api/ai/generate returning 200 even if OpenAI call fails.
        return f"[openai-failed] {prompt.strip()[:2000]}"
