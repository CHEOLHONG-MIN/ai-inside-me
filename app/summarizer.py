import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAISummaryProvider:
    """OpenAI API 기반 요약기"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")
        self.client = OpenAI(api_key=self.api_key)

    def summarize(self, text: str) -> str:
        """입력된 텍스트를 요약"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # ✅ 최신 경량 GPT 모델 사용
                messages=[
                    {"role": "system", "content": "당신은 문장을 간결하게 요약하는 전문가입니다."},
                    {"role": "user", "content": f"다음 문장을 3문장 이내로 요약해 주세요:\n{text}"}
                ],
                max_tokens=200,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"(요약 중 오류 발생: {e})"
