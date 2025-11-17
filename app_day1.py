from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        result = f"'{user_input}' — 멋진 생각이에요!"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port)
