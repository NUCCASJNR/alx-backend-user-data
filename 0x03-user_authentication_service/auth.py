#!/usr/bin/env python3

"""
Authentication Module
"""

import bcrypt

from db import DB, User, NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hash a password for a user
    :param password: the password to be hashed
    :return:
        The hashed password
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers An Authenticated user to the database
        :param email: User's email address
        :param password: User's password
        :return:
            Registered user obj
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            self._db.add_user(email, hashed_pwd)
