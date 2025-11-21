import os
from flask import Flask
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

from app.config import Config
from app.models import db
from app.routes.main import bp as main_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # DB 초기화
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Flask 3.1+ 호환

    # 블루프린트 등록
    app.register_blueprint(main_bp)

    return app
