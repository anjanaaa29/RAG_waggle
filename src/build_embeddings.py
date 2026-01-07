import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

INPUT_FILE = "data/chunks.json"
INDEX_FILE = "data/faiss_index.index"
TEXT_FILE = "data/chunks_texts.json"

# to load chunks
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk['text'] for chunk in chunks]

# to generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype('float32')

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  
index.add(embeddings)

# to save FAISS index and texts
faiss.write_index(index, INDEX_FILE)
with open(TEXT_FILE, "w", encoding="utf-8") as f:
    json.dump(texts, f)

print(f"Saved FAISS index to {INDEX_FILE} with {len(texts)} chunks.")

