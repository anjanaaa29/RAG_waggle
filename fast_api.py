from fastapi import FastAPI
from pydantic import BaseModel
from src.rag_api import generate_answer

app = FastAPI(title="MyWaggle FAQ RAG API")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    answer = generate_answer(req.question)
    return {"answer": answer}
