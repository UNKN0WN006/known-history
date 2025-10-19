# History RecALI

**Privacy-first browser history summarizer with semantic search and credibility scoring**

Built for MLH Open Source Hackfest using:
- **Google Gemini** (summarization & tagging)
- **Hugging Face Inference API** (trust/credibility scoring)
- **Snowflake** (embeddings storage - planned)
- **Auth0** (opt-in cloud sync - planned)
- **DigitalOcean Gradient** (inference deployment - planned)

## Problem
Browsing history is hard to search and lacks context. Users can't easily recall "that article I read last month about X."

## Solution
History RecALI captures pages you visit, generates AI summaries with credibility scores, and enables semantic search over your personal browsing history — all **privacy-first** (local by default, opt-in sync).

## Features (MVP Demo)
- Browser extension (Chrome MV3)
- One-click page summarization (Gemini API)
- Trust/credibility score (HF zero-shot classification)
- Local storage (chrome.storage.local, zero server by default)
- Semantic search (Snowflake embeddings - in progress)
- Opt-in cloud sync (Auth0 - in progress)

## Quick Start

### Prerequisites
- Python 3.10+
- Chrome/Edge browser
- API keys: [Gemini](https://mlh.link/gemini-quickstart), [HF](https://huggingface.co/settings/tokens)

### Setup (5 min)
```bash
git clone https://github.com/UNKN0WN006/known-history.git
cd known-history
cp .env.example .env
# edit .env with your keys

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```
