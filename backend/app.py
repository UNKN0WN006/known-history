import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# ensure backend is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services import gemini

app = FastAPI(title="History RecALI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_origin_regex="^chrome-extension://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

class SummarizeRequest(BaseModel):
    url: str
    title: str
    snippet: str

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        summary = gemini.summarize_text(req.snippet)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        from backend.services import gradient
        return gradient.score_content(req.text)
    except:
        return {"label": "neutral", "score": 0.5}