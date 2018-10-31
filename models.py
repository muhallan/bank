from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from app import app

db = SQLAlchemy(app)


class User(db.Model):
    """
    The user model. This represents the holder of the bank account
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    account_number = db.Column(db.Integer, db.ForeignKey(
        'account.account_number'), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    account = db.relationship("account",
                              backref=db.backref("user", uselist=False))

    def __init__(self, username, password, name, account_number):
        """
        Initialize the user instance
        """
        self.username = username
        self.password = password
        self.name = name
        self.account_number = account_number

    def save(self):
        """
        Save the user instance to the database
        :return: Boolean
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def get_all():
        """
        Get all the users in the table
        :return: List
        """
        return User.query.all()


class Account(db.Model):
    """
    This is the account model. It represents the bank account of a user
    """
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Integer, unique=True, nullable=False)
    account_balance = db.Column(db.Integer, default=0)
    name = db.Column(db.String(120), db.ForeignKey('user.name'))
    transactions = db.relationship('transaction', backref='account', lazy=True)

    def __init__(self, account_number):
        """
        Initialize the account instance
        """
        self.account_number = account_number

    def save(self):
        """
        Save the account instance to the database
        :return: Boolean
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def get_all():
        """
        Get all the accounts in the table
        :return: List
        """
        return Account.query.all()


class Transaction(db.Model):
    """
    The transaction model. This represents the bank transactions that are
    done by the users on their accounts
    """
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer)
    account_number = db.Column(db.Integer, db.ForeignKey(
        'account.account_number'), nullable=False)

    def __init__(self, type, amount):
        """
        Initialize the transaction instance
        """
        self.type = type
        self.amount = amount

