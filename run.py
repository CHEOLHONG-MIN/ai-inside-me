from app import create_app

app = create_app()

if __name__ == "__main__":
    # 필요 시 포트/호스트 조정 가능
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
