from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
import logging
from auth.decorator import authorization
from constants import DEPOSIT
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
                result = transaction.deposit(amount)
                if result:
                    response = {
                        'status': 'success',
                        'message': "Deposit made successfully."
                    }
                    return make_response(jsonify(response)), 201
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


# define the API resources
registration_view = DepositView.as_view('deposit_api')

# add Rules for API Endpoints
transaction_blueprint.add_url_rule(
    '/deposit',
    view_func=registration_view,
    methods=['POST']
)
