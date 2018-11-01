import unittest
from app import app, config_dict
from flask_testing import TestCase


class TestProductionConfig(TestCase):
    """
    Test the production configuration
    """
    def create_app(self):
        app.config.from_object(config_dict['production'])
        return app

    def test_app_is_running_on_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is
                         'averyrandomstringthatshardtodecode')


class TestTestingConfig(TestCase):
    """
    Test the testing configuration
    """
    def create_app(self):
        app.config.from_object(config_dict['testing'])
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] is
                         'averyrandomstringthatshardtodecode')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'sqlite:///bank_testing_db'
        )


class TestDevelopmentConfig(TestCase):
    """
    Test the development configuration
    """
    def create_app(self):
        app.config.from_object(config_dict['development'])
        return app

    def test_app_is_running_on_development(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is
                         'averyrandomstringthatshardtodecode')
        self.assertTrue(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertTrue(app.config['SQLALCHEMY_ECHO'])


if __name__ == '__main__':
    unittest.main()
