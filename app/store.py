# backend/store.py
import os
import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self, path="../data/vector_store"):
        self.client = chromadb.PersistentClient(path=path, settings=Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(name="ece_concepts")
        print(f"✅ Vector store initialized at {path}")

    def add_documents(self, docs, embeddings):
        """Store docs with embeddings"""
        ids = [str(i) for i in range(len(docs))]
        self.collection.add(documents=docs, embeddings=embeddings.tolist(), ids=ids)
        print(f"🧠 Stored {len(docs)} chunks in vector DB.")

    def retrieve_similar_docs(self, query_embedding, top_k=3):
        """Retrieve top-k relevant chunks"""
        results = self.collection.query(query_embeddings=[query_embedding.tolist()], n_results=top_k)
        docs = results["documents"][0]
        return docs

