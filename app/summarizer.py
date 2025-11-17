import re

class SummaryProvider:
    def summarize(self, text: str) -> str:
        raise NotImplementedError

class LocalSummaryProvider(SummaryProvider):
    def summarize(self, text: str, max_len: int = 240) -> str:
        text = re.sub(r"\s+", " ", text.strip())
        if not text:
            return "요약할 텍스트가 없습니다."
        sentences = re.split(r'(?<=[.!?…\n])\s+', text)
        draft = " ".join(sentences[:2])
        summary = draft[:max_len] + ("..." if len(draft) > max_len else "")
        if len(summary) < 40 and len(text) > 40:
            words = [w for w in re.split(r"[^가-힣A-Za-z0-9]+", text) if w]
            top = " ".join(words[:5])
            summary += f" (핵심어: {top})"
        return f"(로컬 요약) {summary}"

def text_stats(text: str) -> dict:
    import re
    chars = len(text)
    words = len([w for w in re.split(r"\W+", text) if w])
    import re as _re
    sentences = len(_re.findall(r"[.!?…]", text)) or 1
    return {"chars": chars, "words": words, "sentences": sentences}
