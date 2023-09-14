#!/usr/bin/env python3

"""
Flask App
"""

from flask import (
    abort, Flask, jsonify, redirect, request
)
from werkzeug import Response

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
def logout_user() -> Response:
    """
    LOgs out a user
    :return:
        redirect to the '/' route
    """
    session_id = request.cookies.get('session_id')
    find_user = AUTH.get_user_from_session_id(session_id)
    if not find_user:
        abort(403)
    AUTH.destroy_session(find_user)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def view_profile():
    """
    View users profile
    :return:
        user obj
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    reset user pwd
    :return:
        message
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    Updates a user pwd
    :return: message
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_pwd = request.form.get('new_password')
    try:
        if reset_token:
            AUTH.update_password(reset_token, new_pwd)
            return jsonify({"email": f"{email}",
                            "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
