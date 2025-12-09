from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import timedelta

import os
from openai import OpenAI

class OpenAISummaryProvider:
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        print("🔍 DEBUG: 현재 환경변수 목록 일부 =", list(os.environ.keys())[:20])
        print("🔍 DEBUG: OPENAI_API_KEY =", api_key[:8] + "..." if api_key else "None")

        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY가 .env 파일이나 Railway Variables에 설정되어 있지 않습니다.")
        self.client = OpenAI(api_key=api_key)


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///summaries.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv("SECRET_KEY", "dev_secret")

    app.permanent_session_lifetime = timedelta(minutes=30)

    # ✅ app이 정의된 다음에 init_app()을 호출해야 합니다.
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # 라우트 등록
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # DB 테이블 생성
    with app.app_context():
        db.create_all()

    return app

# Flask-Login user loader
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
