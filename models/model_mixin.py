from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from app import app

db = SQLAlchemy(app)


class ModelMixin(db.Model):
    """
    Base model that contains save and delete methods, and common field
    attributes in the models
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        """
        Save an instance of the model to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def delete(self):
        """
        Delete an instance of the model from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @classmethod
    def fetch_all(cls):
        """
        Return all the data in the model.
        """
        return cls.query.all()

    @classmethod
    def get(cls, *args):
        """
        Return data filtered by the id.
        """
        return cls.query.get(*args)

    @classmethod
    def order_by(cls, *args):
        """
        Query and order the data of the model by the given args.
        """
        return cls.query.order_by(*args)

    @classmethod
    def filter_all(cls, **kwargs):
        """
        Query and filter the data of the model by the given kwargs.
        """
        return cls.query.filter(**kwargs).all()

    @classmethod
    def filter_and_order(cls, *args, **kwargs):
        """
        Query, filter and order the data of the model using the given args
        and kwargs.
        """
        return cls.query.filter_by(**kwargs).order_by(*args)
