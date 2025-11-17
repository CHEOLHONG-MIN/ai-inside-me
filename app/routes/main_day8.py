from flask import Blueprint, render_template, request, abort
from app.models import db, Summary
from app.summarizer import LocalSummaryProvider, text_stats

bp = Blueprint("main", __name__)
summary_provider = LocalSummaryProvider()

@bp.get("/")
def home():
    return render_template("index.html")

@bp.post("/summarize")
def summarize():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", error="요약할 텍스트가 없습니다.")
    if len(text) > 5000:
        return render_template("index.html", error="입력이 너무 깁니다. 5,000자 이하로 넣어주세요.")
    summary = summary_provider.summarize(text)
    stats = text_stats(text)
    new_summary = Summary(text=text, summary=summary)
    db.session.add(new_summary)
    db.session.commit()
    return render_template("index.html", summary=summary, stats=stats)

@bp.get("/history")
def history():
    summaries = Summary.query.order_by(Summary.created_at.desc()).limit(10).all()
    return render_template("history.html", summaries=summaries)

@bp.get("/history/<int:summary_id>")
def summary_detail(summary_id: int):
    s = Summary.query.get(summary_id)
    if not s:
        abort(404)
    return render_template("detail.html", s=s)
