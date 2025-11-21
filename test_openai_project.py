from dotenv import load_dotenv
import os
from openai import OpenAI

# ✅ .env 파일 로드
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID")
)

try:
    models = client.models.list()
    print("✅ API Key 연결 성공!")
    for m in models.data[:3]:
        print(" -", m.id)
except Exception as e:
    print("❌ 연결 실패:", e)
