#!/usr/bin/env python3

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
