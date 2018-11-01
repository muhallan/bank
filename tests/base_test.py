from flask_testing import TestCase
from app import app, db, config_dict


class BaseTestCase(TestCase):
    """
    Base test class
    """

    def create_app(self):
        app.config.from_object(config_dict['testing'])
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
