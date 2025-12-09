import os
from openai import OpenAI

class OpenAISummaryProvider:
    def __init__(self):
        # 1️⃣ Railway 환경 변수 직접 확인 (os.environ 사용)
        api_key = os.environ.get("OPENAI_API_KEY")

        # 2️⃣ Key 없을 때 에러 표시
        if not api_key:
            print("❌ 환경변수 OPENAI_API_KEY가 감지되지 않았습니다.")
            print("현재 환경변수 목록:", list(os.environ.keys()))
            raise ValueError("❌ OPENAI_API_KEY가 .env 파일이나 Railway Variables에 설정되어 있지 않습니다.")

        # 3️⃣ 정상일 때 클라이언트 초기화 
         self.client = OpenAI(api_key=api_key)

    def summarize(self, text):
        # GPT 호출
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "아래 글의 핵심 내용을 간단히 요약하세요."},
                {"role": "user", "content": text}
            ],
        )
        return response.choices[0].message.content.strip()
