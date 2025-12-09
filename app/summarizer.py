import os
from openai import OpenAI


class OpenAISummaryProvider:
    def __init__(self):
        # 1️⃣ Railway 환경 변수 확인
        api_key = os.environ.get("OPENAI_API_KEY")
        print("✅ DEBUG: OPENAI_API_KEY =", api_key[:8] + "..." if api_key else "None")

        # 2️⃣ 키가 없을 경우 오류 처리
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY가 .env 파일이나 Railway Variables에 설정되어 있지 않습니다.")

        # 3️⃣ OpenAI 클라이언트 생성
        self.client = OpenAI(api_key=api_key)

    def summarize(self, text):
        """텍스트를 요약하는 메서드"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "아래 글의 핵심 내용을 간결하게 요약하세요."},
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content.strip()
