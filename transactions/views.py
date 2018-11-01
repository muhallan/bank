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


class CheckBalance(MethodView):
    """
    View to help the user check their balance
    """
    @authorization
    def get(self, *args, **kwargs):
        # get the user's id from the decorator data
        user_id = kwargs['user_id']
        account = Account.find_first(user_id=user_id)
        balance = account.check_balance()
        response = {
            'status': 'success',
            'account_balance': balance,
            'message': f"Your account number is: {account.account_number}"
        }
        return make_response(jsonify(response)), 200


class TransactionHistory(MethodView):
    """
    View to show the user's transaction history
    """
    @authorization
    def get(self, *args, **kwargs):
        # get the user's id from the decorator data
        user_id = kwargs['user_id']
        account = Account.find_first(user_id=user_id)
        history = account.get_transaction_history()
        all_history = []
        for transanction in history:
            data = {
                'date': transanction.date,
                'type': transanction.type,
                'amount': transanction.amount
            }
            all_history.append(data)

        response = {
            'status': 'success',
            'transaction_history': all_history,
            'message': f"Your account number is: {account.account_number}"
        }
        return make_response(jsonify(response)), 200


# define the API resources
deposit_view = DepositView.as_view('deposit_api')
withdraw_view = WithdrawView.as_view('withdraw_api')
check_balance = CheckBalance.as_view('check_balance_api')
transaction_history = TransactionHistory.as_view('transaction_history_api')


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
transaction_blueprint.add_url_rule(
    '/check_balance',
    view_func=check_balance,
    methods=['GET']
)
transaction_blueprint.add_url_rule(
    '/transaction_history',
    view_func=transaction_history,
    methods=['GET']
)
