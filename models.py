from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # account_number = db.Column(db.Integer, db.ForeignKey(
    #     'account.account_number'), nullable=False)
    name = db.Column(db.String(120), nullable=False)


# class Account(db.Model):
#     __tablename__ = 'account'
