#!/usr/bin.env python3
"""
Contains session db auth
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    session db auth
    """

    def create_session(self, user_id=None):
        """
        Overload create session
        :param user_id: user_id
        :return:
            session_id
        """
        session_id = super().create_session(user_id)
        if not isinstance(session_id, str):
            return None
        session = UserSession(session_id=session_id, user_id=user_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Overloads user_id_for_session_id
        :param session_id: session_id for the session
        :return:
            user_id based on the session_id
        """
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if not sessions or len(sessions) <= 0:
            return None
        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id
        created_at = session.created_at
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """
        overloads destroy_session
        :param request: request obj
        :return: An empty {}
        """
        cookie = self.session_cookie(request)
        if not cookie:
            return False
        try:
            sessions = UserSession.search({"session_id": cookie})
        except Exception:
            return False
        if len(sessions):
            return False
        session = sessions[0]
        session.remove()
        return True
