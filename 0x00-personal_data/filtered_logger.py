#!/usr/bin/env python3
"""Contains a filtering function"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """
    Obfuscates the sensitive fields in a log message.
    """
    for field in fields:
        if field in message:
            message = re.sub(r"{}=.*?{}".format(field, separator),
                             '{}={}{}'.format(field, redaction, separator),
                             message)
    return message
