from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from blog import db, app
from blog.forms import LoginForm, PostForm
from blog.models import Post, User
from blog.utils import title_slugifier, save_picture



@app.route("/")
def start():
    return render_template("home.html")
@app.route("/password", methods = ["POST", "GET"])
def password():
    attempt = str(request.form["pw_input"])
    if attempt == "6414":
        return redirect(url_for("home"))
    else:
        flash("Hai sbagliato mammoccio")

    return redirect(url_for("start"))

@app.route("/h")
def home():
    from random import randint
    LAST_W = "Ci dispiace, non c'è ancora nessuna notizia qui!"
    LAST = Post.query.all()[-1]
    rand_n = randint(1, (LAST.id-1))
    RANDOM = Post.query.filter_by(id=rand_n).first()
    return render_template("home.html", last=LAST, random=RANDOM, last_w=LAST_W)



@app.route("/pres-news")
def pres_news():
    page_number = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page_number, per_page=4, error_out=True)

    if posts.has_next:
        next_page = url_for("pres_news", page=posts.next_num)
    else:
        next_page = None
    if posts.has_prev:
        previous_page = url_for("pres_news", page=posts.prev_num)
    else:
        previous_page = None
    
    return render_template("Pres_news.html", posts=posts, current_page=page_number,
                            next_page=next_page, previous_page=previous_page)

@app.route("/posts/<string:post_slug>")
def article(post_slug):
    post_instance = Post.query.filter_by(slug=post_slug).first_or_404()
    return render_template("article.html", post=post_instance)






@app.route("/create-article", methods=["GET", "POST"])
@login_required
def create_article():
    form = PostForm()
    if form.validate_on_submit():
        slug = title_slugifier(form.title.data)
        new_post = Post(title=form.title.data, body=form.body.data, slug=slug,
                       description = form.description.data, author=current_user)

        if form.cover.data:
            try:
                cover = save_picture(form.cover.data)
                new_post.cover = cover
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("article", post_slug=slug))
    return render_template("post_editor.html", form=form)

@app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_article(post_id):
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_instance.title = form.title.data
        post_instance.description = form.description.data
        post_instance.body = form.body.data

        if form.cover.data:
            try:
                cover = save_picture(form.cover.data)
                post_instance.cover = cover
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))


        db.session.commit()
        return redirect(url_for("article", post_slug=post_instance.slug))
    elif request.method == "GET":
        form.title.data = post_instance.title
        form.description.data = post_instance.description
        form.body.data = post_instance.body
    return render_template("post_editor.html", form=form)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_article(post_id):
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    db.session.delete(post_instance)
    db.session.commit()
    return redirect(url_for("pres_news"))






@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Username e  password non combaciano")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("home"))
    
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
