from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from blog import db, app
from blog.forms import LoginForm, PostForm
from blog.models import Post, User


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
def article(post_id):
    post_instance = Post.query.get_or_404(post_id)
    return render_template("article.html", post=post_instance)



@app.route("/create-article", methods=["GET", "POST"])
@login_required
def create_article():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, body=form.body.data,
                       description = form.description.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("article", post_id=new_post.id))
    return render_template("post_editor.html.html", form=form)

@app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_article(post_id):
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    form = PostForm
    if form.validate_on_submit():
        post_instance.title = form.title.data
        post_instance.description = form.description.data
        post_instance.body = form.body.data
        db.session.commit()
        return redirect(url_for("article", post_id=post_instance.id))
    elif request.method == "GET":
        form.title.data = post_instance.title
        form.description.data = post_instance.description
        form.body.data = post_instance.body
    return render_template("post_editor.html")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_article(post_id):
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    db.session.delete(post_instance)
    db.session.commit()



@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.html"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Username e  password non combaciano")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("home.html"))
    
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return render_template("login.html")