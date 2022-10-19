from flask import render_template, request, flash
from blog import app
from blog.models import Post


@app.route("/")
def home():

    return render_template("home.html")

@app.route("/password", methods = ["POST", "GET"])
def password():
    attempt = str(request.form["pw_input"])
    if attempt == "6414":
        flash("Welcome, sir.")
    else:
        flash("Hai sbagliato mammoccio")

    return render_template("home.html")

@app.route("/pres-news")
def pres_news():
    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("Pres_news.html", posts=posts)

@app.route("/posts/<int:post_id>")
def pres_article(post_id):
    post_instance = Post.query.get_or_404(post_id)
    return render_template("pres_article.html", post=post_instance)