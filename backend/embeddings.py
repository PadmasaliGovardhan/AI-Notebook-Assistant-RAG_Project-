# backend/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingManager:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        print(f"✅ Loaded embedding model: {model_name}")

    def generate_embeddings(self, texts):
        """Generate embeddings for a list of text chunks"""
        return np.array(self.model.encode(texts, show_progress_bar=True))

