#!/usr/bin/env python3
"""Contains a function for generating hashed passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Generates a hashed password
    :return:
            A salted hashed password
    """
    # Encode the password to bytes since bcrypt.hashpw requires
    # a byte and the salted
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    :param hashed_password:
    :param password:
    :return:
        TRue or False
    """
    encoded = password.encode("utf-8")
    if bcrypt.checkpw(encoded, hashed_password):
        return True
    return False
