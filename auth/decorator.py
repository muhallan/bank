from flask import request, jsonify, make_response
from functools import wraps
from models.models import User


def authorization(func):
    @wraps(func)
    def check_authorization(*args, **kwargs):
        # check if the header with key is present
        if 'Authorization' not in request.headers:
            response = {
                'status': 'fail',
                'message': 'Header with key Authorization missing.'
            }
            return make_response(jsonify(response)), 401

        # Get the access token from the header
        auth_header = request.headers.get('Authorization').strip()

        # check for when authorization was not provided in header
        if not auth_header:
            response = {
                'status': 'fail',
                'message': ('Token not provided in the header with key '
                            'Authorization.')
            }
            return make_response(jsonify(response)), 401

        auth_strings = auth_header.split(" ")
        if len(auth_strings) != 2:
            response = {
                'status': 'fail',
                'message': 'Invalid token format.'
            }
            return make_response(jsonify(response)), 401

        access_token = auth_header.split(" ")[1]

        if access_token:
            # Attempt to decode the token and get the user ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                kwargs['user_id'] = user_id

                return func(*args, **kwargs)

            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'status': 'fail',
                'message': message
            }
            return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'Empty token string'
            }
            return make_response(jsonify(response)), 401

    check_authorization.__doc__ = func.__doc__
    return check_authorization
