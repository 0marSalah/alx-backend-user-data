#!/usr/bin/env python3
""" Auth
"""
from bcrypt import hashpw, gensalt
from typing import Any


def _hash_password(password: str) -> Any:
    """ hash password
    """
    return hashpw(password.encode('utf-8'), gensalt())
