from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
import os

from .rag_app import RAGApp  # relative import

app = FastAPI(title="Personal Assistant")
rag = RAGApp()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = os.path.abspath(os.getcwd())
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
    filename = os.path.basename(file.filename)
    path = os.path.join(UPLOAD_DIR, filename)
    try:
        with open(path, "wb") as f:
            f.write(await file.read())
        text = extract_text_from_pdf(path)
        chunks = rag.add_notes(text)
        return {"status": "success", "message": f"{chunks} chunks added from {filename}"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post("/ask/")
async def ask_question(query: str = Form(...)):
    answer = rag.ask(query)
    return {"question": query, "answer": answer}

