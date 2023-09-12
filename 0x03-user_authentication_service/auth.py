#!/usr/bin/env python3

"""
Authentication module
"""

import bcrypt

from db import DB, User, NoResultFound
import uuid


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
    generated_id = str(uuid.uuid4())
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
            Registered user obj
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
        """
        Create session
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
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
        if not user_id:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except NoResultFound:
            pass
