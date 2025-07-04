from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI(title="AI Text Summarizer")

class SummarizerRequest(BaseModel):
    text: str
    model: str

@app.post("/summarize")
async def summarizer(request: SummarizerRequest):
    return {"summary": f"Placeholder summary for text: {request.text} using model: {request.model}"}