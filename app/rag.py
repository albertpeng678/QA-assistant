"""RAG 核心邏輯 — 本檔是學員要補完的「核心缺口」。

tests/test_rag.py 內有現成的失敗測試，你的目標是讓它們全部通過：
    pytest tests/test_rag.py -v

提示與參考見 README.md 的「缺口地圖」。完整答案在 solution branch：
    git show solution:app/rag.py
"""


def parse_response(response):
    """把 Responses API 回應解析為 {"answer": str, "citations": [str]}。

    🎯 缺口 1（核心，有測試）：實作此函式，讓 test_rag.py 的 parse_response 測試通過。
    """
    raise NotImplementedError("缺口 1：請實作 parse_response — 提示見 README")


def answer_question(client, question, *, vector_store_id, model):
    """以 file_search tool 對 vector store 提問，回傳 answer + citations。

    🎯 缺口 2（核心，有測試）：呼叫 OpenAI Responses API 的 file_search tool，
    再用 parse_response 解析結果。
    """
    raise NotImplementedError("缺口 2：請實作 answer_question — 提示見 README")
