from unittest import TestCase
from app import app


class TestProductionConfig(TestCase):
    """
    Test the production configuration
    """

    def create_app(self):
        app.config.from_object('production')
        return app

    def test_app_is_running_on_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
