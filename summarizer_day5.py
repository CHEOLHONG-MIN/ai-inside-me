# summarizer.py
import re

class SummaryProvider:
    def summarize(self, text: str) -> str:
        raise NotImplementedError

class LocalSummaryProvider(SummaryProvider):
    """API 없이 동작하는 간단 요약기 (휴리스틱)"""
    def summarize(self, text: str, max_len: int = 240) -> str:
        text = re.sub(r"\s+", " ", text.strip())
        if not text:
            return "요약할 텍스트가 없습니다."
        # 1) 문장 분할 후 앞부분 골라내기
        sentences = re.split(r'(?<=[.!?…\n])\s+', text)
        draft = " ".join(sentences[:2])  # 앞 1~2문장
        # 2) 길이 제한
        summary = draft[:max_len]
        if len(draft) > max_len:
            summary += "..."
        # 3) 너무 짧으면 핵심 키워드 보강
        if len(summary) < 100 and len(text) > 100:
            words = [w for w in re.split(r"[^가-힣A-Za-z0-9]+", text) if w]
            top = " ".join(words[:5])
            summary += f" (핵심어: {top})"
        return f"(로컬 요약) {summary}"

def text_stats(text: str) -> dict:
    chars = len(text)
    words = len([w for w in re.split(r"\W+", text) if w])
    sentences = len(re.findall(r"[.!?…]", text)) or 1
    return {"chars": chars, "words": words, "sentences": sentences}
