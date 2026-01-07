import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# groq API key
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client_llm = Groq(api_key=GROQ_API_KEY)

# Load FAISS index and chunk texts
INDEX_FILE = "data/faiss_index.index"
TEXT_FILE = "data/chunks_texts.json"

index = faiss.read_index(INDEX_FILE)
with open(TEXT_FILE, "r", encoding="utf-8") as f:
    texts = json.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

TOP_K = 5

def retrieve_chunks(query, top_k=TOP_K):
    query_emb = model.encode([query]).astype('float32')
    distances, indices = index.search(query_emb, top_k)
    return [texts[i] for i in indices[0]]

def generate_answer(query, chunks):
    context_text = "\n".join(chunks)
    prompt = f"""
You are an expert assistant. Read the FAQ context below and provide a detailed, step-by-step, and user-friendly and concize answer to the question. 
Include explanations and examples if possible. Avoid repeating the context verbatim. If the question doesn't exist in the FAQ say the question does not exist, don't over explain.

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

def main():
    print("=== MyWaggle FAQ Chatbot (FAISS + Groq) ===")
    print("Type 'exit' to quit\n")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            break

        chunks = retrieve_chunks(user_query)
        if not chunks:
            print("Bot: Sorry, no relevant FAQ found.\n")
            continue

        answer = generate_answer(user_query, chunks)
        print(f"Bot: {answer}\n")

if __name__ == "__main__":
    main()



