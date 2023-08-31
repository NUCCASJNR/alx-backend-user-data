#!/usr/bin/env python3
"""Contains a filtering function"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """
    Obfuscates the sensitive fields in a log message.
    """
    return re.sub(fr'({"|".join(map(re.escape, fields))})=.*?;',
                  fr'\1={redaction}{separator}', message)
