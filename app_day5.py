from flask import Flask, render_template, request
from models import db, Summary
from summarizer import LocalSummaryProvider, text_stats
import os
from dotenv import load_dotenv

# ✅ 환경변수 로드 및 앱 초기화
load_dotenv()
app = Flask(__name__)

# ✅ DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///summaries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

summary_provider = LocalSummaryProvider()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", error="요약할 텍스트가 없습니다.")
    summary = summary_provider.summarize(text)
    stats = text_stats(text)

    # ✅ DB 저장
    new_summary = Summary(text=text, summary=summary)
    db.session.add(new_summary)
    db.session.commit()

    return render_template("index.html", summary=summary, stats=stats)

# ✅ 기록 조회 페이지 추가
@app.route("/history")
def history():
    summaries = Summary.query.order_by(Summary.created_at.desc()).limit(10).all()
    return render_template("history.html", summaries=summaries)

# ✅ Flask 3.1 호환: 실행 시 테이블 생성
if __name__ == "__main__":
    with app.app_context():
        print("Creating tables if not exist...")
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
