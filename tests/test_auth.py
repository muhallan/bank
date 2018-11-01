import json
from tests.base_test import BaseTestCase
from models.models import User


def register_user(self, username=None, password=None, name=None):
    return self.client.post(
        '/api/v1/auth/register',
        data=json.dumps(dict(
            username=username,
            password=password,
            name=name
        )),
        content_type='application/json',
    )


def login_user(self, username, password):
    return self.client.post(
        '/api/v1/auth/login',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json',
    )


class TestAuth(BaseTestCase):
    def test_registration(self):
        """
        Test for successful user registration
        """
        with self.client:
            response = register_user(self, 'van.home', 'jhdsdfd', 'van')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registration_with_already_registered_username(self):
        """
        Test registration with an already registered username fails
        """
        user = User(
            username='jimmy',
            password='testpd',
            name='star'
        )
        user.save()
        with self.client:
            response = register_user(self, 'jimmy', 'truthy', 'justice')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def test_registration_fails_with_missing_user_info(self):
        """
        Test that the user doesn't register with a missing user field
        """
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == (
                'Incomplete data. Ensure valid data for username, name '
                'and password are provided'))
            self.assertFalse(data.get('auth_token'))
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

            response = register_user(self, 'my username')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == (
                'Incomplete data. Ensure valid data for username, name '
                'and password are provided'))
            self.assertFalse(data.get('auth_token'))
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

            response = register_user(self, password='some pswd', name='a name')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == (
                'Incomplete data. Ensure valid data for username, name '
                'and password are provided'))
            self.assertFalse(data.get('auth_token'))
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

            response = register_user(self, username='some username',
                                     password='', name='a name')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == (
                'Incomplete data. Ensure valid data for username, name '
                'and password are provided'))
            self.assertFalse(data.get('auth_token'))
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
