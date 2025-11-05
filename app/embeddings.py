# app/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingManager:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        print(f"✅ Loaded embedding model: {model_name}")

    def generate_embeddings(self, texts):
        """Generate embeddings for a list of text chunks"""
        # Returns a numpy array of embeddings
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

