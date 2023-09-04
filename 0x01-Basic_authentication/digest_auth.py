#!/usr/bin/env python3

from flask import Flask
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "john": "password1",
    "susan": "password2"
}

# A dictionary to store nonce values for each user
nonces = {}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@auth.generate_nonce
def generate_nonce():
    # Generate a unique nonce for each request
    import uuid
    nonce = str(uuid.uuid4())

    # Store the nonce for the current user
    username = auth.username()
    nonces[username] = nonce

    return nonce


@app.route('/')
@auth.login_required
def index():
    # Get the authenticated username
    username = auth.username()

    # Get the nonce for the current user
    nonce = nonces.get(username, '')

    return f"Hello, {username}! Nonce: {nonce}"


if __name__ == '__main__':
    app.run()
