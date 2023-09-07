#!/usr/bin/env python3

"""
This module handles session id expiration
"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that inherits from SessionAuth
    """

    def __init__(self):
        """
        Initialization method
        """
        try:
            sess_duration = int(getenv('SESSION_DURATION'))
            self.session_duration = sess_duration
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Overloads create session
        :param user_id: id for the user
        :return:
            the session_id
        """
        session_id = super().create_session(user_id)
        session_dictionary = {}
        if not session_id:
            return None
        SessionAuth.user_id_by_session_id[session_id] = session_dictionary
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        overloads user_id_for_session_id
        :param session_id:
        :return:
        """
        if not session_id:
            return None
        session_dict = SessionExpAuth.user_id_for_session_id(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if not created_at:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return session_dict.get('user_id')
