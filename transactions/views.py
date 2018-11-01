from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
import logging


class DepositView(MethodView):
    """
    View to provide the depositing functionality
    """
    def post(self):
        # get the post data
        post_data = request.json
        amount = post_data.get('amount')
        if amount:
            try:
                amount = float(amount.strip())
            except ValueError as e:
                logging.error(f"An error has occurred - {e}")
                response = {
                    'status': 'fail',
                    'message': "Invalid data for amount. Ensure it's a number."
                }
                return make_response(jsonify(response)), 400
        response = {
            'status': 'fail',
            'message': "Please the amount in figures to deposit."
        }
        return make_response(jsonify(response)), 400
