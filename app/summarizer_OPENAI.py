from openai import OpenAI
import os

class OpenAISummaryProvider:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID")  # ✅ 조직 ID 명시
        )

    def summarize(self, text: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 간결하고 정확한 요약을 생성하는 비서입니다."},
                    {"role": "user", "content": f"다음 텍스트를 요약해줘:\n\n{text}"}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"(요약 중 오류 발생) {e}"
