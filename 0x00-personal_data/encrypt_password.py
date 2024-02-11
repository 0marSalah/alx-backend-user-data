#!/usr/bin/env python3
""" Encrypt password """


def filter_datum(fields, redaction, message, separator):
    """ returns the log message obfuscated """
    for field in fields:
        message = message.replace(field + separator,
                                  redaction + separator)
    return message
