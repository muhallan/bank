import json
import unittest
from tests.base_test import BaseTestCase


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
            self.assertEqual(response.status_code, 200)
            self.assertTrue(res['status'] == 'success')
            self.assertTrue(res['message'] == 'Deposit made successfully.')
            self.assertEqual(res['account_balance'], 550000)

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
            self.assertEqual(response.status_code, 401)
            self.assertTrue(res['status'] == 'fail')
            self.assertTrue(res['message'] == 'Invalid token format.')


class TestWithdraw(BaseTestCase):

    def test_authenticated_user_withdraw_successfully(self):
        """
        Test that a user who is authenticated in can withdraw successfully
        """
        with self.client:
            register_user(self)
            result = login_user(self)
            access_token = json.loads(result.data.decode())['auth_token']
            data = json.dumps({'amount': '550000'})
            # first make a deposit using a POST request
            response = self.client.post(
                '/api/v1/deposit/',
                headers=dict(Authorization="Bearer " + access_token),
                data=data,
                content_type='application/json'
            )
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(res['status'] == 'success')
            self.assertTrue(res['message'] == 'Deposit made successfully.')
            self.assertEqual(res['account_balance'], 550000)

            data_withdraw = json.dumps({'amount': '50000'})
            # first make a deposit using a POST request
            response_withdraw = self.client.post(
                '/api/v1/withdraw/',
                headers=dict(Authorization="Bearer " + access_token),
                data=data_withdraw,
                content_type='application/json'
            )
            res_withdraw = json.loads(response_withdraw.data.decode())
            self.assertEqual(response_withdraw.status_code, 200)
            self.assertTrue(res_withdraw['status'] == 'success')
            self.assertTrue(
                res_withdraw['message'] == 'Withdrawal completed successfully.')
            self.assertEqual(res_withdraw['account_balance'], 500000)

    def test_authenticated_user_over_withdrawal_unsuccessful(self):
        """
        Test that a user who is authenticated can't withdraw more than
        what's in their account
        """
        with self.client:
            register_user(self)
            result = login_user(self)
            access_token = json.loads(result.data.decode())['auth_token']
            data = json.dumps({'amount': '550000'})
            # first make a deposit using a POST request
            response = self.client.post(
                '/api/v1/deposit/',
                headers=dict(Authorization="Bearer " + access_token),
                data=data,
                content_type='application/json'
            )
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(res['status'] == 'success')
            self.assertTrue(res['message'] == 'Deposit made successfully.')
            self.assertEqual(res['account_balance'], 550000)

            data_withdraw = json.dumps({'amount': '3050000'})
            # first make a deposit using a POST request
            response_withdraw = self.client.post(
                '/api/v1/withdraw/',
                headers=dict(Authorization="Bearer " + access_token),
                data=data_withdraw,
                content_type='application/json'
            )
            res_withdraw = json.loads(response_withdraw.data.decode())
            self.assertEqual(response_withdraw.status_code, 400)
            self.assertTrue(res_withdraw['status'] == 'fail')
            self.assertTrue(
                res_withdraw['message'] == (
                    'Amount to withdraw is greater than available balance.')
            )

    def test_unauthenticated_user_withdraw_fail(self):
        """
        Test that a user who is not authenticated can't withdraw successfully
        """
        with self.client:
            data = json.dumps({'amount': '550000'})
            # make a deposit using a POST request
            response = self.client.post(
                '/api/v1/withdraw/',
                headers=dict(Authorization="Bearer "),
                data=data,
                content_type='application/json'
            )
            res = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(res['status'] == 'fail')
            self.assertTrue(res['message'] == 'Invalid token format.')


if __name__ == '__main__':
    unittest.main()
