from dotenv import load_dotenv
load_dotenv()  # ← .env를 Flask보다 먼저 로드

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
