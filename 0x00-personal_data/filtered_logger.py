#!/usr/bin/env python3
"""Contains a filtering function"""

import logging
import re
from typing import List, Tuple
from os import getenv
import mysql.connector

PII_FIELDS: Tuple = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filters incoming records
        :param record:
        :return:
            filtered result
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates the sensitive fields in a log message.
    """
    for field in fields:
        if field in message:
            message = re.sub(r"{}=.*?{}".format(field, separator),
                             '{}={}{}'.format(field, redaction, separator),
                             message)
    return message


def get_logger() -> logging.Logger:
    """
    :return:
        logging.logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """:returns a secured connection"""
    username: str = getenv("PERSONAL_DATA_DB_USERNAME")
    password: str = getenv("PERSONAL_DATA_DB_PASSWORD")
    host: str = getenv("PERSONAL_DATA_DB_HOST")
    database: str = getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )
    return connection
