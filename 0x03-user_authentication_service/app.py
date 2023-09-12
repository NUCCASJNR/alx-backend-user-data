#!/usr/bin/env python3

"""
Flask App
"""

from flask import (
    Flask, jsonify, request, Response
)
from auth import Auth
app = Flask(__name__)
auth = Auth()


@app.route('/')
def index() -> Response:
    """
    Index route
    :return:
        Jsonified Message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """
    Adds a new user to the database
    :return:
        The added user obj
    """
    email = request.form['email']
    password = request.form['password']
    try:
        auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)