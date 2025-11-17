from flask import Flask, render_template, request
import os, re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def local_fallback_summary(text: str, max_len: int = 200) -> str:
    # 아주 단순한 로컬 요약(첫 문장 몇 개 + 길이 제한)
    sentences = re.split(r'(?<=[.!?…])\s+', text.strip())
    draft = " ".join(sentences[:2]) if sentences else text
    return f"(로컬 요약) {draft[:max_len]}"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", summary="요약할 텍스트가 없습니다.")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Korean text concisely."},
                {"role": "user", "content": f"다음 한국어 텍스트를 2~3문장으로 간결히 요약해줘:\n\n{text}"}
            ],
            temperature=0.2,
            max_tokens=300
        )
        summary = completion.choices[0].message.content.strip()

    except Exception as e:
        msg = str(e)
        if "insufficient_quota" in msg or "You exceeded your current quota" in msg:
            summary = local_fallback_summary(text)
        else:
            summary = f"요약 중 오류가 발생했습니다: {e}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
