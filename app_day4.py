from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from summarizer import LocalSummaryProvider, text_stats  # ← 추가

load_dotenv()
app = Flask(__name__)

# 오늘은 로컬 프로바이더(모의 AI)로 고정
summary_provider = LocalSummaryProvider()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", error="요약할 텍스트가 없습니다.")

    # 입력 길이 간단 제한 (UX 보호)
    if len(text) > 5000:
        return render_template("index.html", error="입력이 너무 깁니다. 5,000자 이하로 넣어주세요.")

    # 로컬 요약 + 통계
    summary = summary_provider.summarize(text)
    stats = text_stats(text)
    return render_template("index.html", summary=summary, stats=stats)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
