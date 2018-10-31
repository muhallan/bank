from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    account_number = db.Column(db.Integer, db.ForeignKey(
        'account.account_number'), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    account = db.relationship("account",
                              backref=db.backref("user", uselist=False))


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Integer, unique=True, nullable=False)
    account_balance = db.Column(db.Integer)
    name = db.Column(db.String(120), db.ForeignKey('user.name'))
    transactions = db.relationship('transaction', backref='account', lazy=True)


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer)
    account_number = db.Column(db.Integer, db.ForeignKey(
        'account.account_number'), nullable=False)

