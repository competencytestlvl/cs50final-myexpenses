# from application import db
import datetime as dt
from . import db
from flask_login import UserMixin


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=dt.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    # date_created = db.Column(db.DateTime, default=dt.datetime.utcnow)
    # Establish 1 to many relationship
    transactions = db.relationship('Expenses', lazy=True)

    # Create custom application string representation
    def __repr__(self):
        return f"User {self.id}"