#!/usr/bin/env python3

"""
Flask App
"""

from flask import (
    abort, Flask, jsonify, redirect, request, Response
)
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


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
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login_user():
    """
    Logs in a user
    :return:
        user obj
    """
    email = request.form['email']
    password = request.form['password']
    if AUTH.valid_login(email, password):
        created_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", created_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout_user() -> str:
    """
    LOgs out a user
    :return:
        redirect to the '/' route
    """
    session_id = request.cookies['session_id']
    find_user = AUTH.get_user_from_session_id(session_id)
    if find_user:
        AUTH.destroy_session(find_user)
        return redirect('/')
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
