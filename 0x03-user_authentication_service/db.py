#!usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str):
        """
        Adds a new user to the database
        :param email: user's email address
        :param hashed_password: user's hashed pwd
        :return:
            User obj
        """
        user_dict = {"email": email,
                     "hashed_password": hashed_password}
        user_obj = User(**user_dict)
        self._session.add(user_obj)
        self._session.commit()
        return user_obj