from flask import Blueprint, render_template, request, abort, redirect, url_for
from app.models import db, Summary
from app.summarizer import OpenAISummaryProvider

from flask import jsonify

bp = Blueprint("main", __name__)
summary_provider = OpenAISummaryProvider()

@bp.get("/")
def home():
    return render_template("index.html")

@bp.get("/history")
def history():
    page = int(request.args.get("page", 1))
    q = request.args.get("q", "").strip()

    query = Summary.query.order_by(Summary.created_at.desc())
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Summary.text.ilike(like)) | (Summary.summary.ilike(like))
        )

    per_page = 5
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    total = query.count()
    has_prev = page > 1
    has_next = page * per_page < total

    return render_template(
        "history.html",
        summaries=items,
        page=page,
        has_prev=has_prev,
        has_next=has_next,
        q=q,
    )

@bp.post("/summarize")
def summarize():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", error="요약할 텍스트를 입력하세요.")

    # 로컬 요약기 사용 (API 없이)
    summary_provider = LocalSummaryProvider()
    summary = summary_provider.summarize(text)

    # DB에 저장
    s = Summary(text=text, summary=summary)
    db.session.add(s)
    db.session.commit()

    return render_template("index.html", summary=summary)


@bp.get("/history/<int:summary_id>")
def summary_detail(summary_id: int):
    s = Summary.query.get_or_404(summary_id)
    return render_template("detail.html", s=s)

@bp.get("/history/<int:summary_id>/delete")
def delete_summary(summary_id: int):
    s = Summary.query.get_or_404(summary_id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("main.history"))

@bp.post("/api/summarize")
def api_summarize():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "요약할 텍스트를 입력하세요."}), 400

    # ✅ OpenAI 기반 요약기 사용
    summary_provider = OpenAISummaryProvider()
    summary = summary_provider.summarize(text)

    # DB 저장
    s = Summary(text=text, summary=summary)
    db.session.add(s)
    db.session.commit()

    return jsonify({
        "summary": summary,
        "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
        "id": s.id
    })
