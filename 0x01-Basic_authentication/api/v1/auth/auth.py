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
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Handles path
        :param path:
        :param excluded_paths:
        :return:
            False-Path
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
        return True

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
