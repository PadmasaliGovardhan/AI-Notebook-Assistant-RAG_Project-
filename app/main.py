# backend/main.py
from dotenv import load_dotenv
load_dotenv()  # loads .env file

from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
import os
from rag_app import RAGApp

app = FastAPI(title="Personal Assistant")
rag = RAGApp()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "../data/notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text
    

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    text = extract_text_from_pdf(path)
    chunks = rag.add_notes(text)
    return {"status": "success", "message": f"{file.filename} Uploaded Sucessfully...."}


@app.post("/ask/")
async def ask_question(query: str = Form(...)):
    answer = rag.ask(query)
    return {"question": query, "answer": answer}
def main():
    print("Hello from rag-demo!")


if __name__ == "__main__":
    main()
