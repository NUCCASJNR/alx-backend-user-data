#!/usr/bin/env python3
"""Contains a filtering function"""

import logging
import re
from typing import List, Tuple
import os
import mysql.connector

PII_FIELDS: Tuple = ("name", "email", "phone", "ssn", "password")

USERNAME: str = os.getenv("PERSONAL_DATA_DB_USERNAME")
PASSWORD: str = os.getenv("PERSONAL_DATA_DB_PASSWORD")
HOST: str = os.getenv("PERSONAL_DATA_DB_HOST")
DATABASE: str = os.getenv("PERSONAL_DATA_DB_NAME")


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
    connection = mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    return connection


def main() -> None:
    """"
    Main function that returns nothing
    """
    connection = get_db()
    # Create the cursor object
    cursor = connection.cursor()
    # Perform query
    cursor.execute("SELECT * FROM users")
    selected_rows = cursor.fetchall()
    logger = get_logger()
    for row in selected_rows:
        print(row)
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
