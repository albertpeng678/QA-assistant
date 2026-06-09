def parse_response(response):
    """把 Responses API 回應解析為 answer 與去重後的 citations。"""
    answer_parts = []
    citations = []
    for item in response.output:
        content = getattr(item, "content", None)
        if not content:
            continue
        for part in content:
            text = getattr(part, "text", None)
            if text:
                answer_parts.append(text)
            for ann in getattr(part, "annotations", []) or []:
                filename = getattr(ann, "filename", None)
                if filename and filename not in citations:
                    citations.append(filename)
    return {"answer": "".join(answer_parts), "citations": citations}
