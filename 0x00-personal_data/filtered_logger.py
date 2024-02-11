#!/usr/bin/env python3
""" Encrypt password """
import re


def filter_datum(fields, redaction, message, separator):
    """ returns the log message obfuscated
    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all fields in the log line (message)
    The function should use a regex to replace occurrences of certain field values.
    filter_datum should be less than 5 lines long and use re.sub to perform the substitution with a single regex.
    """
    return re.sub(r'(?<=^|;)\s*(' + '|'.join(fields) + ')=.*?(?=(;|$))',
                  lambda x: x.group().replace(x.group().split('=')[1], redaction), message)
