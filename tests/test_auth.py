import json
import unittest
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


def login_user(self, username=None, password=None):
    return self.client.post(
        '/api/v1/auth/login',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json',
    )


class TestAuth(BaseTestCase):
    def test_registration_successful(self):
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

    def test_registered_user_login_successfully(self):
        """
        Test the successful login of a registered user
        """
        with self.client:
            # user registration
            response = register_user(self, 'van.home', 'jhdsdfd', 'van')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(
                data['message'] == 'Successfully registered.'
            )
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

            # registered user login
            response_login = login_user(self, 'van.home', 'jhdsdfd')
            data_login = json.loads(response_login.data.decode())
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(response_login.content_type == 'application/json')
            self.assertEqual(response_login.status_code, 200)

    def test_non_registered_user_login(self):
        """
        Test that login of a non-registered user fails
        """
        with self.client:
            response = login_user(self, 'joe@bloggs.com', 'ppejdsd')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_missing_login_data(self):
        """
        Test that login with incomplete user data fails
        """
        with self.client:
            response = login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Username or password '
                                               'not provided.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

            response = login_user(self, username='ham')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Username or password '
                                               'not provided.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

            response = login_user(self, password='jam')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Username or password '
                                               'not provided.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
