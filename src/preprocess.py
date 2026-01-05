import json
import os
import re

INPUT_FILE = "data/faqs.txt"
OUTPUT_FILE = "data/chunks.json"

CHUNK_SIZE = 500   # characters
CHUNK_OVERLAP = 50


def clean_text(text):
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks


def main():
    os.makedirs("data", exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned_text = clean_text(raw_text)
    chunks = chunk_text(cleaned_text, CHUNK_SIZE, CHUNK_OVERLAP)

    # Save chunks as JSON
    chunk_data = [{"id": i, "text": chunk} for i, chunk in enumerate(chunks)]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunk_data, f, indent=2)

    print(f"Created {len(chunks)} chunks")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
