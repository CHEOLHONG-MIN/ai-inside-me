import pytest
from app import create_app
from app.models import db, Summary

@pytest.fixture
def client():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)        # ← 텍스트로 받기
    assert "요약할 문장을" in html            # ← b'' 제거

def test_summarize(client):
    text = "AI inside me 프로젝트는 Flask 학습을 위한 단계별 과정입니다."
    resp = client.post("/summarize", data={"text": text})
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "로컬 요약" in html                 # ← b'' 대신 문자열

def test_history(client):
    """히스토리 페이지가 열리는지 확인"""
    response = client.get("/history")
    assert response.status_code == 200
