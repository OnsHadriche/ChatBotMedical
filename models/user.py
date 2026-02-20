from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id           = db.Column(db.Integer, primary_key=True)
    fullname     = db.Column(db.String(150), nullable=False)
    email        = db.Column(db.String(150), unique=True, nullable=False)
    phone        = db.Column(db.String(20),  nullable=True)
    password     = db.Column(db.String(256), nullable=False)
    newsletter   = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.email}>'