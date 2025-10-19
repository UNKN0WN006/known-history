import os
import json
import requests
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# load .env from repo root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://api.openai.com/v1/responses")

def summarize_text(text: str) -> str:
    """
    Minimal Gemini proxy. Replace payload/response parsing with the real Gemini schema.
    """
    if not GEMINI_API_KEY:
        return "ERROR: GEMINI_API_KEY not set in .env"

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gemini-1.5",  # adjust if needed
        "input": f"Summarize the following text in 3 short bullet points and give 3 tags:\n\n{text}"
    }

    resp = requests.post(GEMINI_API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # best-effort extraction — adapt to real response format
    if isinstance(data, dict):
        # try common patterns
        for key in ("summary", "output", "result"):
            if key in data:
                return data[key]
        # nested common places
        for k in ("choices", "outputs", "responses"):
            if k in data and isinstance(data[k], list) and data[k]:
                item = data[k][0]
                for tkey in ("text", "content", "output"):
                    if isinstance(item, dict) and item.get(tkey):
                        return item.get(tkey)
    # fallback
    return json.dumps(data)