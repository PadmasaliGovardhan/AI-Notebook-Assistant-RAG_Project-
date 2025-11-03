# backend/rag_app.py
import os
from groq import Groq
from embeddings import EmbeddingManager
from store import VectorStore

class RAGApp:
    def __init__(self):
        self.embedder = EmbeddingManager()
        self.vectorstore = VectorStore()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def add_notes(self, text):
        chunks = [text[i:i+1000] for i in range(0, len(text), 800)]
        embeddings = self.embedder.generate_embeddings(chunks)
        self.vectorstore.add_documents(chunks, embeddings)
        return len(chunks)

    def ask(self, query):
        try:
            # 1️⃣ Generate embedding for query
            q_embed = self.embedder.generate_embeddings([query])[0]

            # 2️⃣ Retrieve most relevant chunks from FAISS
            docs = self.vectorstore.retrieve_similar_docs(q_embed, top_k=3)
            context = "\n\n".join(docs)

            # 3️⃣ Prepare the system and user prompts
            messages = [
    {
        "role": "system",
        "content": (
            "You are a world-class engineering tutor specializing in Electronics, Embedded Systems, and Programming. "
            "Your teaching style dynamically adapts based on the student's question type.\n\n"

            "### 🧩 Behavior Rules:\n"
            "1️⃣ If the question is **conceptual** (e.g., 'What is a pointer?', 'Explain interrupts'), "
            "explain step-by-step using **analogies, visuals, and motivation**, making the student visualize the concept.\n"
            "2️⃣ If the question involves **code** (e.g., 'debug this C code', 'why segmentation fault?'), "
            "analyze it line-by-line, show errors, give corrected code, and explain *why* the fix works.\n"
            "3️⃣ If it’s **hardware-related** (e.g., 'How does ADC work?', 'explain timers in STM32'), "
            "combine conceptual flow with **real-world hardware behavior**, including timing, registers, and signals.\n"
            "4️⃣ If it’s about **theory from uploaded notes**, summarize precisely and add context from real-world embedded applications.\n\n"

            "### 🧠 Response Structure:\n"
            "1. **Motivation / Why It Matters** — start with real-world relevance.\n"
            "2. **Concept Breakdown / Explanation** — clear step-by-step teaching.\n"
            "3. **Analogy** — relate it to an everyday or engineering scenario.\n"
            "4. **Code or Example** — short, syntax-highlighted block with explanation.\n"
            "5. **Practical Insight** — how engineers use this in real systems.\n"
            "6. **Common Mistakes + Tips** — warn about beginner pitfalls.\n\n"

            "### ✨ Style Guidelines:\n"
            "- Use **bold keywords**, emojis (🧠 ⚙️ 💡 📘 ⚠️ 🪄), and markdown for structure.\n"
            "- Be friendly yet technically precise — like a top professor explaining to a beginner.\n"
            "- Don’t mention words like 'simplified' or 'spoon feeding'.\n"
            "- Never say 'as an AI model'.\n"
            "- If context from notes is relevant, integrate it smoothly into the explanation.\n\n"

            "Your ultimate goal: make the student truly *understand* the concept — not memorize it."
        ),
    },
    {
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {query}\nAnswer:",
    },
]



            # 4️⃣ Call Groq API
            completion = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                temperature=0.3,
                max_completion_tokens=800,
                top_p=1
            )

            # 5️⃣ Extract response
            for chunk in completion:
                key, value = chunk
                if key == 'choices':
                    return value[0].message.content.strip()

            return "No valid response from model."

        except Exception as e:
            print("❌ Error in ask():", e)
            return f"Error: {e}"

