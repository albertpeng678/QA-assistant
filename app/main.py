from fastapi import FastAPI, Depends
from pydantic import BaseModel, field_validator
from openai import OpenAI

from app import config
from app.rag import answer_question

app = FastAPI(title="法規 RAG 問答")

class AskRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("question 不可為空")
        return v.strip()

def get_answerer():
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    def answerer(question: str):
        return answer_question(
            client, question,
            vector_store_id=config.VECTOR_STORE_ID,
            model=config.OPENAI_MODEL,
        )
    return answerer

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/ask")
def ask(req: AskRequest, answerer=Depends(get_answerer)):
    return answerer(req.question)
