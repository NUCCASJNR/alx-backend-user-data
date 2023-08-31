#!/usr/bin/env python3

import logging


def add(a, b):
    try:
        result = a + b
        return result
    except Exception as e:
        logging.error("Exception occured", exc_info=True)

def div(a, b):
    try:
        c = a / b
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)


print(add(3, 4))
print(add(2, 6))

(div(5, 0))