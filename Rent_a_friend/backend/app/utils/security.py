# Password hashing, JWT functions, etc.

import hashlib
import jwt
import os
from app.config import SECRET_KEY

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_jwt_token(data: dict) -> str:
    # Creates a JWT token for secure authentication.
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")
