#!/usr/bin/env python3

"""
Flask App
"""

from flask import Flask, jsonify, Response

app = Flask(__name__)


@app.route('/')
def index() -> Response:
    """
    Index route
    :return:
        Jsonified Message
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
