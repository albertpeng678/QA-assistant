from fastapi import FastAPI

app = FastAPI(title="法規 RAG 問答")

@app.get("/health")
def health():
    return {"status": "ok"}
