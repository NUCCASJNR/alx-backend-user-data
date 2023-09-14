#!/usr/bin/env python3

"""
Authentication module
"""

import bcrypt

from db import DB, User, NoResultFound
from uuid import uuid4


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


def _generate_uuid() -> str:
    """
    Generates a unique_id
    :return:
        The generated id
    """
    generated_id = str(uuid4())
    return generated_id


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
            Registered user object
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user's login credentials
        :param email: user's email
        :param password: user's pwd
        :return:
            True | False
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                hashed_pwd = user.hashed_password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_pwd):
                    return True
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create a session for a user"""
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves a user from the database using the session_id
        :param session_id: user's session_id
        :return:
            The User obj if found else None
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user session
        :param user_id: User_id that the session would be destroyed
        :return:
            None
        """
        # if not user_id:
        #     return None
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Sends a reset password token to a user
        :param email:
            user email
        :return:
            the generated token
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user pwd
        :param reset_token: user reset token
        :param password: user pwd
        :return:
            None
        """
        try:
            token = self._db.find_user_by(reset_token=reset_token)
            if not token:
                raise ValueError
            hashed_pwd = _hash_password(password)
            self._db.update_user(token.id, hashed_password=hashed_pwd,
                                 reset_token=None)
        except Exception:
            raise ValueError
