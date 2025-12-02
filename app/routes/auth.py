from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')
bcrypt = Bcrypt()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('이미 존재하는 사용자명입니다.')
            return redirect(url_for('auth.register'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash('회원가입 완료! 로그인하세요.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('로그인 성공!')
            return redirect(url_for('main.index'))
        else:
            flash('로그인 실패. 사용자명 또는 비밀번호를 확인하세요.')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃되었습니다.')
    return redirect(url_for('main.index'))
