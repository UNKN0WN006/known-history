from fastapi import FastAPI
from pydantic import BaseModel

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
    return {"summary": "placeholder summary"}