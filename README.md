# 🤖 MyWaggle FAQ RAG Chatbot

A simple **Retrieval-Augmented Generation (RAG) chatbot** built to answer questions from the **MyWaggle FAQ website**.  
It retrieves relevant FAQ content using **FAISS vector search** and generates accurate, context-aware answers using **Groq LLM**.

---

## 🔗 Source Website (FAQ Data)

👉 https://support.mywaggle.com/

---

## 🔄 Workflow (RAG Pipeline)

User Question
↓
Convert question to embedding
↓
FAISS vector search (Top-K FAQ chunks)
↓
Relevant FAQ context
↓
Groq LLM (LLaMA 3.1)
↓
Final Answer shown to user

---

## 🧠 Architecture Overview

- **Retriever**: FAISS (semantic similarity search)
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`)
- **Generator**: Groq LLM
- **Frontend**: Streamlit

---

## 🧩 File Descriptions (One-Liners)

- **scrape_faq.py**  
  Scrapes FAQ questions and answers from the MyWaggle support website.

- **preprocess.py**  
  Cleans the scraped text and splits it into smaller overlapping chunks.

- **build_embeddings.py**  
  Converts text chunks into embeddings and stores them in a FAISS index.

- **rag.py**  
  Handles retrieval of relevant chunks and generates answers using Groq LLM.

- **app.py**  
  Streamlit UI for interacting with the chatbot (question input, answer display, clear button).


---

## 📦 Install Dependencies

### Download & install requirements

```bash
pip install -r requirements.txt
```
---
▶️ Run the Application Locally
streamlit run app.py

🌐 Streamlit Cloud Deployment

Once deployed, the app will be available at:


👉 ](https://ragwaggle-chatbot12345.streamlit.app/)

