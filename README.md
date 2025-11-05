---
title: AI NoteBook Assistant (RAG)
emoji: 📘
colorFrom: indigo
colorTo: yellow
sdk: docker
app_file: backend/main.py
pinned: false
---


# 🧠 AI NoteBook Assistant (RAG)

An **AI-powered RAG-based Notes Assistant** that helps you:
- 📂 Upload notes and textbooks (PDF)
- 🧠 Retrieve context using **FAISS Vector Search**
- 💬 Ask questions — get **step-by-step, real-world explanations**
- ⚙️ Built with **FastAPI**, **Groq LLM**, and **Sentence Transformers**

---

## ⚙️ Tech Stack
- **Backend:** FastAPI + Groq API + FAISS
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Frontend:** HTML / CSS / JS (static interface)
- **Deployed On:** Hugging Face Spaces 🚀

---

## 🧩 Workflow
1️⃣ Upload your notes → chunks are embedded  
2️⃣ Embeddings stored in FAISS vector DB  
3️⃣ When you ask a question → relevant chunks retrieved  
4️⃣ Groq LLM (GPT OSS 20B) generates rich, example-driven answers  

---

🔗 **Live Space:** https://huggingface.co/spaces/gvadxx/AI-NoteBook-Assistant-RAG  
👨‍💻 **Author:** [Padmasali Govardhan](https://www.linkedin.com/in/govardhanpadmasali/)

