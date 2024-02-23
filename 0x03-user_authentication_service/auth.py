#!/usr/bin/env python3
""" Auth
"""
import bcrypt
import uuid
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

    def valid_login(self, email: str, password: str) -> bool:
        """valid login function"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except Exception:
            return False
        
    def _generte_uuid(self) -> str:
        """ generate a uuid"""
        return str(uuid.uuid4())
    
    def create_session(self, email: str) -> str:
        """ create a session"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generte_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None
