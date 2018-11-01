import unittest
from tests.base_test import BaseTestCase, db
from models.models import User


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            username='test_user',
            password='test_password',
            name='test_name'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.generate_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            username='test_user',
            password='test_password',
            name='test_name'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.generate_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_token(auth_token.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()
