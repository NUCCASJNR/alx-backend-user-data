#!/usr/bin/env python3

"""Contains a BasicAuth class that inherits from auth"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic Auth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts Base 64 from Authorization header for Basic Authentication.
        :param authorization_header: The Authorization header string.
        :return: The Base 64 part of the header,
         or None if it doesn't meet the criteria.
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        parts = authorization_header.split()
        if len(parts) == 2 and parts[0] == 'Basic':
            return parts[1]
        return None
