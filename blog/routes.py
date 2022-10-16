from flask import render_template
from blog import app

@app.route("/")
def home():
    posts = [{"title": "primo post", "body": "primo body"},
            {"title": "secondo post", "body": "secondo body"}]
    return render_template("home.html", posts=posts)