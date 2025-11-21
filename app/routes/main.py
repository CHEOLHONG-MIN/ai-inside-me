from flask import Blueprint, render_template, request, jsonify
from markupsafe import Markup   # ✅ Flask 3.x 대응
from sqlalchemy import or_
from app.models import db, Summary
from app.summarizer import LocalSummaryProvider
import re

bp = Blueprint("main", __name__)


# 홈 페이지
@bp.route("/")
def index():
    return render_template("index.html")


# 요약 API (로컬 요약 사용)
@bp.post("/api/summarize")
def api_summarize():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "요약할 텍스트를 입력하세요."}), 400

    summary_provider = LocalSummaryProvider()
    summary = summary_provider.summarize(text)

    s = Summary(text=text, summary=summary)
    db.session.add(s)
    db.session.commit()

    return jsonify({
        "summary": summary,
        "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
        "id": s.id
    })


# 요약 기록 / 검색 / 하이라이트 / 페이지네이션
@bp.route("/history")
def history():
    q = request.args.get("q", "").strip()
    exclude = request.args.get("exclude", "").strip()
    sort_order = request.args.get("sort", "desc")
    page = request.args.get("page", 1, type=int)
    per_page = 5

    query = Summary.query

    # ✅ 검색어 포함 필터
    if q:
        query = query.filter(or_(
            Summary.text.like(f"%{q}%"),
            Summary.summary.like(f"%{q}%")
        ))

    # ✅ 제외 단어 필터
    if exclude:
        query = query.filter(
            ~or_(
                Summary.text.like(f"%{exclude}%"),
                Summary.summary.like(f"%{exclude}%")
            )
        )

    # ✅ 정렬 순서 처리
    if sort_order == "asc":
        query = query.order_by(Summary.created_at.asc())
    else:
        query = query.order_by(Summary.created_at.desc())

    # 페이지네이션
    pagination = query.paginate(page=page, per_page=per_page)
    summaries = pagination.items

    # 검색어 하이라이트 처리
    from markupsafe import Markup
    import re
    if q:
        pattern = re.compile(re.escape(q), re.IGNORECASE)
        for s in summaries:
            s.text = Markup(pattern.sub(f"<mark>{q}</mark>", s.text))
            s.summary = Markup(pattern.sub(f"<mark>{q}</mark>", s.summary))

    return render_template("history.html",
                           summaries=summaries,
                           q=q,
                           exclude=exclude,
                           sort_order=sort_order,
                           pagination=pagination)

# 상세 페이지
@bp.route("/history/<int:summary_id>")
def summary_detail(summary_id):
    summary = Summary.query.get_or_404(summary_id)
    return render_template("detail.html", summary=summary)

@bp.route("/delete/<int:summary_id>", methods=["POST"])
def delete_summary(summary_id):
    summary = Summary.query.get_or_404(summary_id)
    db.session.delete(summary)
    db.session.commit()
    return jsonify({"success": True})

