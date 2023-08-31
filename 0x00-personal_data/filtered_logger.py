#!/usr/bin/env python3

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """
    Obfuscates the sensitive fields in a log message.

    Args:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character is separating all fields in the log line (message).

    Returns:
        The obfuscated log message.
    """
    for field in fields:
        pattern: str = r'({}=).*?;'.format(field)
        replace: str = r'\1{}{}'.format(redaction, separator)
        message = re.sub(pattern, replace, message)
    return message
