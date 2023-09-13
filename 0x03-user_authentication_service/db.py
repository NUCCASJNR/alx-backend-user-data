#!/usr/bin/env python3

"""DB module
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def add_user(self, email: str, hashed_password: str) -> User:
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

    def find_user_by(self, **kwargs) -> User:
        """
        Queries the database and returns the match if found
        :param kwargs: Arbitrary args
        :return:
            Value of the kwargs passed
        """
        if not kwargs:
            raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs)
        query = user.first()
        if not query:
            raise NoResultFound
        return query

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's detail
        :param user_id: user_id of the user to be updated
        :param kwargs: Arbitrary args
        :return:
            The updated user object
        """
        user_to_update = self.find_user_by(id=user_id)
        if not user_to_update:
            return
        for key, value in kwargs.items():
            if hasattr(user_to_update, key):
                setattr(user_to_update, key, value)
            else:
                raise ValueError
        self._session.commit()
