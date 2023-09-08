#!/usr/bin/env python3
"""Contains a sessionAuth class that inherits from Auth"""

from api.v1.auth.auth import Auth
from typing import Dict
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    Session Auth class that inherits from Auth
    Args:
        user_id_by_session_id: stores session id
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session for a user_id
        :param user_id: user_id that a session is being created for
        :return:
            None if user_id is None
            None if user_id is not a string
        """
        if not user_id or not isinstance(user_id, str):
            return None
        generated_uid = str(uuid4())
        SessionAuth.user_id_by_session_id[generated_uid] = user_id
        return generated_uid

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Finds the session_id for a user_id
        :param session_id: session_id of a user
        :return:
            None if session_id is None
            None if session_id is not a string
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a user obj cookie
        :param request: request obj
        :return:
            user's cookie
        """
        session_cookie = self.session_cookie(request)
        try:
            user_id = self.user_id_for_session_id(session_cookie)
            return User.get(user_id)
        except KeyError:
            return None

    def destroy_session(self, request=None):
        """
        Destroys a current session
        :param request: request obj
        :return:
            The deleted cookie
        """
        if not request:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False
        linked = self.user_id_for_session_id(session_cookie)
        if not linked:
            return False
        self.user_id_by_session_id.pop(session_cookie)
        return True
