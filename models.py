from datetime import datetime
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    first_name = db.Column(db.String(180), nullable=False)
    last_name = db.Column(db.String(180), nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    avatar = db.Column(db.String(25), nullable=False, default='default.jpg')
    password = db.Column(db.String(55), nullable=False)
    posts = db.relationship('Classification', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.first_name}','{self.last_name}','{self.email}','{self.avatar}')"

    # encrypt password user
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Classification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Classification('{self.classification}','{self.date_post}')"
