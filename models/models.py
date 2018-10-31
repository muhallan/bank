from .model_mixin import db, ModelMixin


class User(ModelMixin):
    """
    The user model. This represents the holder of the bank account
    """
    __tablename__ = 'user'

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


class Account(ModelMixin):
    """
    This is the account model. It represents the bank account of a user
    """
    __tablename__ = 'account'

    account_number = db.Column(db.Integer, unique=True, nullable=False)
    account_balance = db.Column(db.Integer, default=0)
    name = db.Column(db.String(120), db.ForeignKey('user.name'))
    transactions = db.relationship('transaction', backref='account', lazy=True)

    def __init__(self, account_number):
        """
        Initialize the account instance
        """
        self.account_number = account_number


class Transaction(ModelMixin):
    """
    The transaction model. This represents the bank transactions that are
    done by the users on their accounts
    """
    __tablename__ = 'transaction'

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
