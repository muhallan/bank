import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from .model_mixin import app, db, ModelMixin


class User(ModelMixin):
    """
    The user model. This represents the holder of the bank account
    """
    __tablename__ = 'user'

    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    account = db.relationship(
        "Account", uselist=False, back_populates="user",
        cascade="all, delete-orphan"
    )

    def __init__(self, username, password, name):
        """
        Initialize the user instance
        """
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.name = name

    def password_is_valid(self, password):
        """
        Check the password against its hash to validate it
        """
        return Bcrypt().check_password_hash(self.password, password)

    @staticmethod
    def generate_token(user_id):
        """
        Generates the access token
        """
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=4),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """
        Decodes the access token from the Authorization header.
        """
        try:
            # decode the token using the SECRET environment variable
            payload = jwt.decode(token, app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"


class Account(ModelMixin):
    """
    This is the account model. It represents the bank account of a user
    """
    __tablename__ = 'account'

    account_number = db.Column(db.Integer, unique=True, nullable=False)
    account_balance = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="account")

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
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)
    account = db.relationship('Account', backref='transactions', lazy=True)

    def __init__(self, type, amount):
        """
        Initialize the transaction instance
        """
        self.type = type
        self.amount = amount
