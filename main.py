from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Optional
import json

from pipeline import run_pipeline
from schemas import PipelineOutput

app = FastAPI(
    title="Task Review Agent — Data Ingestion Pipeline",
    description="Deterministic data ingestion and processing pipeline",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/analyze", response_model=PipelineOutput)
async def analyze(
    text: str = Form(..., description="Task description text"),
    file: Optional[UploadFile] = File(None, description="Optional PDF or JSON file")
):
    """
    Main pipeline endpoint.
    Accepts text + optional file, returns fully structured signals.
    """
    # --- Validate input ---
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty.")

    file_content = None
    file_type = None

    if file and file.filename:
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in ["pdf", "json"]:
            raise HTTPException(status_code=400, detail="Only PDF or JSON files are supported.")
        file_type = ext
        file_content = await file.read()
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    result = run_pipeline(text=text, file_content=file_content, file_type=file_type)
    return result


@app.get("/health")
def health():
    return {"status": "ok", "pipeline": "deterministic"}
