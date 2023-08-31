#!/usr/bin/env python3

import logging

class RedactingFormatter(logging.Formatter):
    def format(self, record):
        # Redact sensitive data before formatting the log message
        message = super().format(record)
        message = message.replace('SECRET_PASSWORD', '********')
        message = message.replace('API_KEY', '********')
        return message

# Create a logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Create a StreamHandler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# Create a redacting formatter
formatter = RedactingFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the StreamHandler
stream_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(stream_handler)

# Log a message with sensitive data
logger.info('User logged in with API_KEY: ABC123 and PASSWORD: SECRET_PASSWORD')
