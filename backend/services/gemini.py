import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# load .env from repo root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://api.openai.com/v1/responses")

def summarize_text(text: str) -> str:
    """
    Minimal Gemini proxy. Raises if GEMINI_API_KEY missing.
    Adapt request/response parsing to the real Gemini API schema if needed.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set in .env")

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gemini-1.5",
        "input": f"Summarize the following text in 3 short bullet points and provide 3 tags:\n\n{text}"
    }

    resp = requests.post(GEMINI_API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # best-effort extraction — adapt to real response format
    summary = None
    if isinstance(data, dict):
        # direct fields
        for key in ("summary", "output", "result", "text"):
            if key in data and data[key]:
                summary = data[key]
                break

        # nested outputs/choices/responses
        if not summary:
            for container in ("choices", "outputs", "responses"):
                items = data.get(container)
                if isinstance(items, list) and items:
                    first = items[0]
                    if isinstance(first, dict):
                        for tkey in ("text", "content", "output", "response"):
                            if first.get(tkey):
                                summary = first.get(tkey)
                                break
                        if summary:
                            break

    if not summary:
        # fallback: stringify response
        summary = json.dumps(data, ensure_ascii=False)

    # truncate reasonably for UI
    return summary if len(summary) <= 2000 else summary[:2000] + "..."