from dotenv import load_dotenv
load_dotenv()
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
import os


# keep package-relative import if this is inside app/
from .rag_app import RAGApp
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
app = FastAPI(title="Personal Assistant")

# Initialize RagApp safely
try:
    rag = RAGApp()
except Exception as e:
    rag = None
    print("Initialization error in RagApp:", e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use a writable, ephemeral path suitable for Spaces
UPLOAD_DIR = "/tmp/notes"
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

        if rag is None:
            return {"status": "error", "detail": "Server initialization failed. RagApp not ready."}

        text = extract_text_from_pdf(path)
        if not text.strip():
            return {"status": "error", "detail": "Uploaded PDF contains no extractable text."}

        chunks = rag.add_notes(text)
        return {"status": "success", "message": f"{chunks} chunks added from {filename}"}
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "detail": str(e),
            "traceback": traceback.format_exc()
        }

@app.post("/ask/")
async def ask_question(query: str = Form(...)):
    if rag is None:
        return {"status": "error", "detail": "Server initialization failed. RagApp not ready."}
    answer = rag.ask(query)
    return {"question": query, "answer": answer}

