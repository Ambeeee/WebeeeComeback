from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from alerter import send_confirm
from blog import db, app
from blog.forms import LoginForm, PostForm, UserForm
from blog.models import User, PresPost, Wpost
from blog.utils import title_slugifier, save_picture





#WEBEEE
@app.route("/")
def home():
    from random import randint
    try: LAST_W = Wpost.query.all()[-1]
    except: LAST_W = Wpost.query.filter_by(id=1).first()
    try: LAST = PresPost.query.all()[-1]
    except: LAST = PresPost.query.filter_by(id=1).first()
    first = PresPost.query.first()
    try: rand_n = randint(first.id, (LAST.id-1))
    except: rand_n = 1
    RANDOM = PresPost.query.filter_by(id=rand_n).first()
    from version import recorded_version
    version = recorded_version()
    
    return render_template("home.html", last=LAST, random=RANDOM, last_w=LAST_W, version=version)

@app.route("/news")
def webeee_news():
    page_number = request.args.get("page", 1, type=int)
    posts = Wpost.query.order_by(Wpost.created_at.desc()).paginate(page=page_number, per_page=3, error_out=True)

    if posts.has_next:
        next_page = url_for("webeee_news", page=posts.next_num)
    else:
        next_page = None
    if posts.has_prev:
        previous_page = url_for("webeee_news", page=posts.prev_num)
    else:
        previous_page = None
    
    return render_template("webeee_news.html", posts=posts, current_page=page_number,
                            next_page=next_page, previous_page=previous_page)

@app.route("/news/<string:post_slug>")
def webeee_article(post_slug):
    post_instance = Wpost.query.filter_by(slug=post_slug).first_or_404()
    from random import choice
    try:
        rand_n = choice([
            a for a in range(PresPost.query.first().id, (PresPost.query.all()[-1].id))
            if a!=post_instance.id] 
            )
    except: rand_n = 1
    RANDOM = PresPost.query.filter_by(id=rand_n).first()
    return render_template("article.html", post=post_instance, adv=RANDOM, readonly=True)

@app.route("/news/create", methods=["GET", "POST"])
@login_required
def create_article():
    form = PostForm()
    new_post = Wpost()
    if form.validate_on_submit():
        slug = title_slugifier(form.title.data)
        new_post = Wpost(title=form.title.data, description = form.description.data,

            body1=form.body1.data, body2=form.body2.data, body3=form.body3.data,
            body4=form.body4.data, body5=form.body5.data,

            testimonial1=form.testimonial1.data, testimonial2=form.testimonial2.data,
            testimonial3=form.testimonial3.data,

            slug=slug, author=current_user)

        if form.cover.data:
            try:
                cover = save_picture(form.cover.data)
                new_post.cover = cover
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))
                
        if form.img1.data:
            try:
                img1 = save_picture(form.img1.data)
                new_post.image1 = img1
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))

        if form.img2.data:
            try:
                img2 = save_picture(form.img2.data)
                new_post.image2 = img2
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))

        if form.img3.data:
            try:
                img3 = save_picture(form.img3.data)
                new_post.image3 = img3
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))


        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("webeee_article", post_slug=slug))
    return render_template("article.html", form=form, post=new_post, editor=True)

@app.route("/news/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_article(post_id):
    post_instance = Wpost.query.get_or_404(post_id)
    if post_instance.author != current_user and current_user.role not in ["BOSS", "webeee_editor"]:
        abort(401)
    form = PostForm()
    if form.validate_on_submit():
        post_instance.title = form.title.data
        post_instance.description = form.description.data
        post_instance.body1 = form.body1.data
        post_instance.body2 = form.body2.data
        post_instance.body3 = form.body3.data
        post_instance.body4 = form.body4.data
        post_instance.body5 = form.body5.data
        post_instance.testimonial1 = form.testimonial1.data
        post_instance.testimonial2 = form.testimonial2.data
        post_instance.testimonial3 = form.testimonial3.data

        if form.cover.data:
            try:
                cover = save_picture(form.cover.data)
                post_instance.cover = cover
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))

        if form.img1.data:
            try:
                img1 = save_picture(form.img1.data)
                post_instance.image1 = img1
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))

        if form.img2.data:
            try:
                img2 = save_picture(form.img2.data)
                post_instance.image2 = img2
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))

        if form.img3.data:
            try:
                img3 = save_picture(form.img3.data)
                post_instance.image3 = img3
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))


        db.session.commit()
        return redirect(url_for("pres_article", post_slug=post_instance.slug))
    elif request.method == "GET":
        form.title.data = post_instance.title
        form.description.data = post_instance.description
        form.body1.data = post_instance.body1
        form.body2.data = post_instance.body2
        form.body3.data = post_instance.body3
        form.body4.data = post_instance.body4
        form.body5.data = post_instance.body5
        form.testimonial1.data = post_instance.testimonial1
        form.testimonial2.data = post_instance.testimonial2
        form.testimonial3.data = post_instance.testimonial3
    return render_template("article.html", form=form, post=post_instance, modify=True)

@app.route("/news/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_article(post_id):
    post_instance = Wpost.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    db.session.delete(post_instance)
    db.session.commit()
    return redirect(url_for("webeee_news"))



#PRES
@app.route("/pres")
def pres():
    return render_template("pres.html")

@app.route("/pres/news")
def pres_news():
    page_number = request.args.get("page", 1, type=int)
    posts = PresPost.query.order_by(PresPost.created_at.desc()).paginate(page=page_number, per_page=3, error_out=True)

    if posts.has_next:
        next_page = url_for("pres_news", page=posts.next_num)
    else:
        next_page = None
    if posts.has_prev:
        previous_page = url_for("pres_news", page=posts.prev_num)
    else:
        previous_page = None
    
    return render_template("pres_news.html", posts=posts, current_page=page_number,
                            next_page=next_page, previous_page=previous_page)

@app.route("/pres/news/<string:post_slug>")
def pres_article(post_slug):
    post_instance = PresPost.query.filter_by(slug=post_slug).first_or_404()
    from random import choice
    try:
        rand_n = choice([
            a for a in range(PresPost.query.first().id, (PresPost.query.all()[-1].id))
            if a!=post_instance.id] 
            )
    except: rand_n = 1
    RANDOM = PresPost.query.filter_by(id=rand_n).first()
    return render_template("article.html", post=post_instance, adv=RANDOM, pres=True, readonly=True)

@app.route("/pres/news/create", methods=["GET", "POST"])
@login_required
def create_pres_article():
    form = PostForm()
    new_post = PresPost()
    if form.validate_on_submit():
        slug = title_slugifier(form.title.data)
        new_post = PresPost(title=form.title.data, description = form.description.data,

            body1=form.body1.data, body2=form.body2.data, body3=form.body3.data,
            body4=form.body4.data, body5=form.body5.data,

            testimonial1=form.testimonial1.data, testimonial2=form.testimonial2.data,
            testimonial3=form.testimonial3.data,

            slug=slug, author=current_user)

        if form.cover.data:
            try:
                cover = save_picture(form.cover.data)
                new_post.cover = cover
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))
                
        if form.img1.data:
            try:
                img1 = save_picture(form.img1.data)
                new_post.image1 = img1
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))

        if form.img2.data:
            try:
                img2 = save_picture(form.img2.data)
                new_post.image2 = img2
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))

        if form.img3.data:
            try:
                img3 = save_picture(form.img3.data)
                new_post.image3 = img3
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=new_post.id))


        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("pres_article", post_slug=slug))
    return render_template("article.html", form=form, post=new_post, editor=True)

@app.route("/pres/news/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_pres_article(post_id):
    post_instance = PresPost.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post_instance.title = form.title.data
        post_instance.description = form.description.data
        post_instance.body1 = form.body1.data
        post_instance.body2 = form.body2.data
        post_instance.body3 = form.body3.data
        post_instance.body4 = form.body4.data
        post_instance.body5 = form.body5.data
        post_instance.testimonial1 = form.testimonial1.data
        post_instance.testimonial2 = form.testimonial2.data
        post_instance.testimonial3 = form.testimonial3.data

        if form.cover.data:
            try:
                cover = save_picture(form.cover.data)
                post_instance.cover = cover
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))

        if form.img1.data:
            try:
                img1 = save_picture(form.img1.data)
                post_instance.image1 = img1
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))

        if form.img2.data:
            try:
                img2 = save_picture(form.img2.data)
                post_instance.image2 = img2
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))

        if form.img3.data:
            try:
                img3 = save_picture(form.img3.data)
                post_instance.image3 = img3
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_article", post_id=post_instance.id))


        db.session.commit()
        return redirect(url_for("pres_article", post_slug=post_instance.slug))
    elif request.method == "GET":
        form.title.data = post_instance.title
        form.description.data = post_instance.description
        form.body1.data = post_instance.body1
        form.body2.data = post_instance.body2
        form.body3.data = post_instance.body3
        form.body4.data = post_instance.body4
        form.body5.data = post_instance.body5
        form.testimonial1.data = post_instance.testimonial1
        form.testimonial2.data = post_instance.testimonial2
        form.testimonial3.data = post_instance.testimonial3
        
    if post_instance.author == current_user or current_user.role == "BOSS":
        return render_template("article.html", form=form, post=post_instance, editor=True)
    
    elif current_user.role == "testimonial" or current_user.role == "webeee_editor":
        return render_template("article.html", form=form, post=post_instance, cit=True)
    
    else:   abort(401)

@app.route("/pres/news/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_pres_article(post_id):
    post_instance = PresPost.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    db.session.delete(post_instance)
    db.session.commit()
    return redirect(url_for("pres_news"))




#USERS
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Username e password non combaciano")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("home"))
    
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/users/manage-users")
def manage_users():
    page_number = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.role).paginate(page=page_number, per_page=10, error_out=True)

    return render_template("manage_users.html", users=users)

@app.route("/users/<string:username>")
@login_required
def user_info(username):
    user_instance = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user_instance)

@app.route("/users/create", methods=["GET", "POST"])
@login_required
def create_user():
    if current_user.role != "BOSS":
        abort(401)
    form = UserForm()
    new_user = User()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
        email=form.email.data, role=form.role.data)
        new_user.set_password_hash(form.password.data)

        db.session.add(new_user)
        db.session.commit()
        send_confirm(new_user.username, new_user.email)
        return redirect(url_for("user_info", username=new_user.username))
    return render_template("user.html", form=form, user=new_user, modify=True)
             
@app.route("/users/<string:username>/edit", methods=["GET", "POST"])
@login_required
def update_user(username):
    user_instance = User.query.filter_by(username=username).first_or_404()
    form = UserForm()
    if form.validate_on_submit():
        user_instance.username = form.username.data
        user_instance.email = form.email.data
        user_instance.role = form.role.data
        user_instance.set_password_hash(form.password.data)

        if form.icon.data:
            try:
                icon = save_picture(form.icon.data)
                user_instance.icon = icon
            except Exception:
                db.session.commit()
                flash("Problema con l'upload.")
                return redirect(url_for("update_user", username=user_instance.username))

        db.session.commit()
        return redirect(url_for("user_info", username=user_instance.username))
    elif request.method == "GET":
        form.username.data = user_instance.username
        form.password.data = user_instance.password
        form.email.data = user_instance.email
        form.role.data = user_instance.role
        form.icon.data = user_instance.icon
    return render_template("user.html", form=form, user=user_instance, modify=True)

@app.route("/users/<string:username>/delete", methods=["POST"])
@login_required
def delete_user(username):
    user_instance = User.query.filter_by(username=username).first_or_404()
    if current_user.role != "BOSS":
        abort(401)
    db.session.delete(user_instance)
    db.session.commit()
    return redirect(url_for("home"))
