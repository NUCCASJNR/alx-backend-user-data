#!/usr/bin/env python3

"""Contains a BasicAuth class that inherits from auth"""
import base64
import binascii
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.base import Base
from models.user import User


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
            return decoded_header.decode('utf-8')
            if decoded_header:
                return decoded_header.decode('utf-8')
            return None
        except binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extract user credentials
        :param decoded_base64_authorization_header:
        :return:
        None, None if decoded_base64_authorization_header is None
        None, None if decoded_base64_authorization_header is not a string
        None, None if decoded_base64_authorization_header doesn’t contain
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' in decoded_base64_authorization_header:
            splited = decoded_base64_authorization_header.split(":", 1)
            # print(splited)
            return splited[0], splited[-1]
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """-
        Handles user's credentials
        :param user_email: user's email which is a string
        :param user_pwd: user's password which is a string
        :return:  None if user_email is None or not a string
        None if user_pwd is None or not a string
        """
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({"email": user_email})
        except Exception as e:
            return None
        if len(user) <= 0:
            return None
        user = user[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overload current_user - and BOOM!
        :param request: HTTP request made
        :return:
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
