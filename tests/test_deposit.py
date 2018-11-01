import json
import unittest
from tests.base_test import BaseTestCase
from models.models import User


def register_user(self, username="user@test", password="test1234",
                  name="tester"):
    """
    Helper method to help register a test user
    """
    user_data = json.dumps({
        'username': username,
        'password': password,
        'name': name
    })
    return self.client.post(
        '/api/v1/auth/register', data=user_data,
        content_type='application/json')


def login_user(self, username="user@test", password="test1234"):
    """
    Helper method to help login a test user
    """
    user_data = json.dumps({
        'username': username,
        'password': password
    })
    return self.client.post(
        'api/v1/auth/login', data=user_data, content_type='application/json')


class TestDeposit(BaseTestCase):

    def test_authenticated_user_deposit_successfully(self):
        """
        Test that a user who is authenticated in can deposit
        """
        with self.client:
            register_user(self)
            result = login_user(self)
            access_token = json.loads(result.data.decode())['auth_token']
            data = json.dumps({'amount': '550000'})
            # make a deposit using a POST request
            response = self.client.post(
                '/api/v1/deposit/',
                headers=dict(Authorization="Bearer " + access_token),
                data=data,
                content_type='application/json'
            )
            res = json.loads(response.data.decode())
            # TODO use check balance to prove that the balance has changed
            self.assertEqual(response.status_code, 201)
            self.assertTrue(res['status'] == 'success')
            self.assertTrue(res['message'] == 'Deposit made successfully.')

    def test_unauthenticated_user_deposit_fail(self):
        """
        Test that a user who is not authenticated can't deposit successfully
        """
        with self.client:
            data = json.dumps({'amount': '550000'})
            # make a deposit using a POST request
            response = self.client.post(
                '/api/v1/deposit/',
                headers=dict(Authorization="Bearer "),
                data=data,
                content_type='application/json'
            )
            res = json.loads(response.data.decode())
            # TODO use check balance to prove that the balance has changed
            self.assertEqual(response.status_code, 401)
            self.assertTrue(res['status'] == 'fail')
            self.assertTrue(res['message'] == 'Invalid token format.')


if __name__ == '__main__':
    unittest.main()
