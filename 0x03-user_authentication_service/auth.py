#!/usr/bin/env python3
""" Auth
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    ''' a function that hashes password'''
    salt = bcrypt.gensalt()
    passWord = password

    hashed_password = bcrypt.hashpw(passWord.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user with the database
        """
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError(f"User {email} already exists")
        return self._db.add_user(email, _hash_password(password))
