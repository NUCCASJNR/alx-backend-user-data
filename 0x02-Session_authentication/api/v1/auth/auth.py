#!/usr/bin/env python3

"""
This module handles how users auth is being managed
"""

from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """
    User auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Handles path
        :param path:
        :param excluded_paths:
        :return:
            True if the path isnt in the excluded_path
            False if it is
        """
        if not path:
            return True
        if not excluded_paths or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        normalized_path = path.rstrip('/')  # Remove trailing slashes
        for paths in excluded_paths:
            # Remove trailing slashes
            normalized_excluded_path = paths.rstrip('/')
            if normalized_path == normalized_excluded_path:
                return False
            stripped = normalized_excluded_path.rstrip('*')
            if normalized_excluded_path.endswith('*'):
                if stripped == normalized_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Authentication Header
        :param request:
        :return:
            The Authentication header else None
        """
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user's info
        :param request:
        :return:
            None
        """
        return None

    def session_cookie(self, request=None):
        """
        Gets the session cookie
        :return:
        :param request: cookie
        :return:
            None if request is None
        """
        if not request:
            return None
        session_id = getenv("SESSION_NAME", "_my_session_id")
        cookie = request.cookies.get(session_id)
        return cookie
