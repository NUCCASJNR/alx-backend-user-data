#!/usr/bin/env python3

"""
Authentication Module
"""

import bcrypt


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
