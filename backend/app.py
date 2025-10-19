from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.services import gemini
import os

app = FastAPI(title="LifeLens Backend")

@app.get("/health")
async def health():
    return {"status":"ok"}

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
