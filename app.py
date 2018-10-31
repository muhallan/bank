from flask import Flask, jsonify

app = Flask(__name__)

from models import db


@app.before_first_request()
def create_tables():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return jsonify('Login route'), 200


if __name__ == '__main__':
    app.run()
