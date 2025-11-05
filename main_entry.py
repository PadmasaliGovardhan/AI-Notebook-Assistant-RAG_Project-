# app.py — entrypoint wrapper used by the Dockerfile / HF build
# This file should live at the *repo root* (same level as app/ directory).

from app.main import app  # import FastAPI app object

