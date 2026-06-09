from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_returns_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

from app.main import app, get_answerer

def test_ask_returns_answer_and_citations():
    def fake_answerer(question):
        return {"answer": f"回答：{question}", "citations": ["a.txt"]}
    app.dependency_overrides[get_answerer] = lambda: fake_answerer
    try:
        resp = client.post("/api/ask", json={"question": "測試問題"})
        assert resp.status_code == 200
        assert resp.json() == {"answer": "回答：測試問題", "citations": ["a.txt"]}
    finally:
        app.dependency_overrides.clear()

def test_ask_rejects_empty_question():
    resp = client.post("/api/ask", json={"question": "  "})
    assert resp.status_code == 422
