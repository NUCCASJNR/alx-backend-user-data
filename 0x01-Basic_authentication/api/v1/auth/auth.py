#!/usr/bin/env python3

"""
This module handles how users auth is being managed
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    User auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> False:
        """
        Handles path
        :param path:
        :param excluded_paths:
        :return:
            False-Path
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Authentication Header
        :param request:
        :return:
            None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user's info
        :param request:
        :return:
            None
        """
        return None
