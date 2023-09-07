#!/usr/bin/env python3

"""
Contains All session Auth routes
"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login_user():
    """
    Logs in a user if it meets all the requirements
    :return:
    the user details
    """
    email_form = request.form.get('email')
    if not email_form or email_form == '':
        return jsonify({"error": "email missing"}), 400
    password_form = request.form.get('password')
    if not password_form or password_form == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email_form})
    if not user:
        return jsonify({"error": "no user found for this email"}), 400
    if not user[0].is_valid_password(password_form):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_name = getenv("SESSION_NAME")
    resp = jsonify(user[0].to_json())
    session_id = auth.create_session(getattr(user[0], 'id'))
    res = resp.set_cookie(session_name, session_id)
    return resp
