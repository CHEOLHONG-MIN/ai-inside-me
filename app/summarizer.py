import os

class LocalSummaryProvider:
    def summarize(self, text: str) -> str:
        sentences = text.split(".")
        if len(sentences) > 2:
            return f"(로컬 요약) {text.split('.')[0].strip()}. {text.split('.')[1].strip()}."
        return f"(로컬 요약) {text.strip()}"
