from types import SimpleNamespace
from app.rag import parse_response

def _fake_response():
    annotation = SimpleNamespace(filename="勞動基準法-第24條.txt")
    content = SimpleNamespace(text="加班費依第24條計算。", annotations=[annotation])
    message = SimpleNamespace(type="message", content=[content])
    file_search_call = SimpleNamespace(type="file_search_call", content=None)
    return SimpleNamespace(output=[file_search_call, message])

def test_parse_response_extracts_answer_and_citations():
    result = parse_response(_fake_response())
    assert result["answer"] == "加班費依第24條計算。"
    assert result["citations"] == ["勞動基準法-第24條.txt"]

def test_parse_response_dedupes_and_handles_no_annotations():
    content = SimpleNamespace(text="無引用的回答。", annotations=[])
    message = SimpleNamespace(type="message", content=[content])
    result = parse_response(SimpleNamespace(output=[message]))
    assert result["answer"] == "無引用的回答。"
    assert result["citations"] == []
