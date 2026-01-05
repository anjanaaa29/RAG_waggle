import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# Load API key
load_dotenv()
client_llm = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load FAISS index and chunk texts
INDEX_FILE = "data/faiss_index.index"
TEXT_FILE = "data/chunks_texts.json"

index = faiss.read_index(INDEX_FILE)

with open(TEXT_FILE, "r", encoding="utf-8") as f:
    texts = json.load(f)

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

TOP_K = 5

def retrieve_chunks(query, top_k=TOP_K):
    query_emb = model.encode([query]).astype("float32")
    _, indices = index.search(query_emb, top_k)
    return [texts[i] for i in indices[0]]

def generate_answer(query):
    chunks = retrieve_chunks(query)

    if not chunks:
        return "The question does not exist in the FAQ."

    context_text = "\n".join(chunks)

    prompt = f"""
You are an expert assistant. Read the FAQ context below and provide a detailed,
step-by-step, user-friendly and concise answer.
If the question does not exist in the FAQ, say so clearly.

Context:
{context_text}

Question: {query}
Answer:
"""

    response = client_llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content.strip()