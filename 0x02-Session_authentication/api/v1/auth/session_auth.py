#!/usr/bin/env python3
"""Contains a sessionAuth class that inherits from Auth"""

from api.v1.auth.auth import Auth
from typing import Dict
from uuid import uuid4


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
