# app.py (root-level file)
from app.main import app

# This is required for Hugging Face to recognize the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

