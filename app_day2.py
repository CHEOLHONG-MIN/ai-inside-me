from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
client = OpenAI()  # 환경변수 OPENAI_API_KEY 를 자동으로 읽습니다.

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "")
    if not text.strip():
        return render_template("index.html", summary="요약할 텍스트가 없습니다.")

    # Responses API 형태의 최소 호출 예시
    resp = client.responses.create(
        model="gpt-5",  # 사용 가능한 최신 텍스트 모델로 교체 가능
        input=f"다음 한국어 텍스트를 한두 문장으로 간결하게 요약해줘:\n{text}"
    )
    summary = resp.output_text.strip()

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port)
