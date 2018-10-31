import os
from flask import Flask, jsonify
from config import config_dict

app = Flask(__name__)
app.config.from_object(config_dict[os.getenv('APP_CONFIG')])

from models.models import db


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return jsonify('Login route'), 200


if __name__ == '__main__':
    app.run()
