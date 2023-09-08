#!/usr/bin/env python3

"""This module contains user session class"""

from models.base import Base


class UserSession(Base):
    """
    User session class that inherits from base
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialization method
        """
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
