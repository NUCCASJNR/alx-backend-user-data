#!/usr/bin/env python3

"""Contains a BasicAuth class that inherits from auth"""
import binascii

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    Basic Auth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts Base 64 from Authorization header for Basic Authentication.
        :param authorization_header: The Authorization header string.
        :return: The Base 64 part of the header,
         or None if it doesn't meet the criteria.
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        parts = authorization_header.split()
        if len(parts) == 2 and parts[0] == 'Basic':
            return parts[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decoded value
        :param base64_authorization_header: value to be decoded
        :return: None if base64_authorization_header is None
        if base64_authorization_header is not a string
            None if base64_authorization_header is not a valid Base64
        """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_header = base64.b64decode(base64_authorization_header)
            if decoded_header:
                return decoded_header.decode('utf-8')
            return None
        except binascii.Error:
            return None
