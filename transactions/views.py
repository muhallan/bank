from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
import logging
from auth.decorator import authorization
from constants import DEPOSIT, WITHDRAW
from models.models import Account, Transaction


transaction_blueprint = Blueprint('transactions', __name__,
                                  url_prefix='/api/v1')


class DepositView(MethodView):
    """
    View to provide the depositing functionality
    """
    @authorization
    def post(self, *args, **kwargs):
        # get the user's id from the decorator data
        user_id = kwargs['user_id']
        # get the post data
        post_data = request.json
        amount = post_data.get('amount')
        if amount:
            try:
                amount = float(amount.strip())
                account = Account.find_first(user_id=user_id)
                transaction = Transaction(
                    type=DEPOSIT,
                    amount=amount,
                    account_id=account.id
                )
                transaction.save()
                result, balance = transaction.deposit(amount)
                if result:
                    response = {
                        'status': 'success',
                        'message': "Deposit made successfully.",
                        'account_balance': balance
                    }
                    return make_response(jsonify(response)), 200
                else:
                    response = {
                        'status': 'fail',
                        'message': "An error has occurred. Please try again."
                    }
                    return make_response(jsonify(response)), 400
            except ValueError as e:
                logging.error(f"An error has occurred - {e}")
                response = {
                    'status': 'fail',
                    'message': "Invalid data for amount. Ensure it's a number."
                }
                return make_response(jsonify(response)), 400
        else:
            response = {
                'status': 'fail',
                'message': "Please provide the amount in figures to deposit."
            }
            return make_response(jsonify(response)), 400


class WithdrawView(MethodView):
    """
    View to provide functionality for withdrawing and deducting money from
    the user's acount
    """
    @authorization
    def post(self, *args, **kwargs):
        # get the user's id from the decorator data
        user_id = kwargs['user_id']
        # get the post data
        post_data = request.json
        amount = post_data.get('amount')
        if amount:
            try:
                amount = float(amount.strip())
                account = Account.find_first(user_id=user_id)
                transaction = Transaction(
                    type=WITHDRAW,
                    amount=amount,
                    account_id=account.id
                )
                transaction.save()
                result, balance = transaction.withdraw(amount)
                if result:
                    response = {
                        'status': 'success',
                        'message': "Withdrawal completed successfully.",
                        'account_balance': balance
                    }
                    return make_response(jsonify(response)), 200
                else:
                    if balance == -1:
                        message = ('Amount to withdraw is greater than '
                                   'available balance.')
                    else:
                        message = "An error has occurred. Please try again."
                    response = {
                        'status': 'fail',
                        'message': message
                    }
                    return make_response(jsonify(response)), 400
            except ValueError as e:
                logging.error(f"An error has occurred - {e}")
                response = {
                    'status': 'fail',
                    'message': "Invalid data for amount. Ensure it's a number."
                }
                return make_response(jsonify(response)), 400
        else:
            response = {
                'status': 'fail',
                'message': "Please provide the amount in figures to withdraw."
            }
            return make_response(jsonify(response)), 400


# define the API resources
deposit_view = DepositView.as_view('deposit_api')
withdraw_view = WithdrawView.as_view('withdraw_api')


# add Rules for API Endpoints
transaction_blueprint.add_url_rule(
    '/deposit',
    view_func=deposit_view,
    methods=['POST']
)
transaction_blueprint.add_url_rule(
    '/withdraw',
    view_func=withdraw_view,
    methods=['POST']
)
