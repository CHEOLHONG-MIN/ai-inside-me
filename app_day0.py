from flask import Flask
import os
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, AI inside me!"

if __name__ == '__main__':
    # 환경 변수에서 PORT 읽기, 기본값 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
