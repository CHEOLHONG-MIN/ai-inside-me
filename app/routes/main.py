from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Summary
from app.summarizer import OpenAISummaryProvider

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def index():
    return render_template("index.html")

@bp.route("/api/summarize", methods=["POST"])
@login_required
def api_summarize():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "요약할 텍스트를 입력하세요."}), 400

    summary_provider = OpenAISummaryProvider()
    summary = summary_provider.summarize(text)

    s = Summary(text=text, summary=summary, user_id=current_user.id)
    db.session.add(s)
    db.session.commit()

    return jsonify({
        "summary": summary,
        "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
        "id": s.id
    })

@bp.route("/history")
@login_required
def history():
    summaries = (
        Summary.query.filter_by(user_id=current_user.id)
        .order_by(Summary.created_at.desc())
        .all()
    )
    return render_template("history.html", summaries=summaries)
