from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from blog import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default="testimonial")
    icon = db.Column(db.String(120))
    pres_post = db.relationship('PresPost', backref='author', lazy='dynamic')
    other_post = db.relationship('Wpost', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"

    def set_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class PresPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(250))
    description = db.Column(db.String(120))

    body1 = db.Column(db.Text, nullable=False)
    body2 = db.Column(db.Text)
    body3 = db.Column(db.Text)
    body4 = db.Column(db.Text)
    body5 = db.Column(db.Text)

    testimonial1 = db.Column(db.Text)
    testimonial2 = db.Column(db.Text)
    testimonial3 = db.Column(db.Text)

    cover = db.Column(db.String(120))
    image1 = db.Column(db.String(120))
    image2 = db.Column(db.String(120))
    image3 = db.Column(db.String(120))
    
    def __repr__(self):
        return f"User('{self.id}', '{self.title}')"

class Wpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(250))
    description = db.Column(db.String(120))

    body1 = db.Column(db.Text, nullable=False)
    body2 = db.Column(db.Text)
    body3 = db.Column(db.Text)
    body4 = db.Column(db.Text)
    body5 = db.Column(db.Text)

    testimonial1 = db.Column(db.Text)
    testimonial2 = db.Column(db.Text)
    testimonial3 = db.Column(db.Text)

    cover = db.Column(db.String(120))
    image1 = db.Column(db.String(120))
    image2 = db.Column(db.String(120))
    image3 = db.Column(db.String(120))
    
    def __repr__(self):
        return f"User('{self.id}', '{self.title}')"





#   flask db migrate -m "messaggio"
#   flask db upgrade
