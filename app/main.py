# app/main.py
from dotenv import load_dotenv
load_dotenv()  # load .env when running locally (safe: don't commit .env)

from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
import os

# relative import from same package
from .rag_app import RAGApp

app = FastAPI(title="Personal Assistant")
# Initialize after dotenv load so keys are available
rag = RAGApp()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep data path inside repo (relative to project root while container runs /code)
ROOT_DIR = os.path.abspath(os.getcwd())  # when container runs, CWD will be /code
UPLOAD_DIR = os.path.join(ROOT_DIR, "data", "notes")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # sanitize filename if needed
    filename = os.path.basename(file.filename)
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    text = extract_text_from_pdf(path)
    chunks = rag.add_notes(text)
    return {"status": "success", "message": f"{chunks} chunks added from {filename}"}

@app.post("/ask/")
async def ask_question(query: str = Form(...)):
    answer = rag.ask(query)
    return {"question": query, "answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

