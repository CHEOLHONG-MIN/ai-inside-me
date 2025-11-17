from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", summary="요약할 텍스트가 없습니다.")
    # 테스트용 가짜 요약
    summary = f"(테스트 요약) {text[:50]}..."
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
