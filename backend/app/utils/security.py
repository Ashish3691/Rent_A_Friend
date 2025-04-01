from fastapi import FastAPI, HTTPException, Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, MONGODB_URI
from pymongo import MongoClient
from typing import Optional
from uuid import uuid4
from services import database
from motor.motor_asyncio import AsyncIOMotorClient
import pytest
from jose.exceptions import ExpiredSignatureError, JWTError

app = FastAPI()

# ✅ Connect to MongoDB

client = AsyncIOMotorClient(MONGODB_URI)
database = client["rent_a_friend_user"]
revoked_tokens_collection = database.get_collection("revoked_tokens")

# ✅ Create a TTL index (auto-remove expired tokens)
revoked_tokens_collection.create_index("revoked_at", expireAfterSeconds=3600)

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


client = MongoClient("mongodb://localhost:27017/")
db = client["auth_db"]
revoked_tokens_collection = db["revoked_tokens"]

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Creates a JWT access token with a unique jti (JWT ID)"""
    to_encode = data.copy()
    jti = str(uuid4())  # Unique identifier
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire, "jti": jti})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def is_token_blacklisted(jti: str) -> bool:
    """Check if token's jti exists in the blacklist collection"""
    return revoked_tokens_collection.find_one({"jti": jti}) is not None

def blacklist_access_token(jti: str):
    """Add token's jti to the blacklist collection"""
    revoked_tokens_collection.insert_one({"jti": jti, "revoked_at": datetime.utcnow()})


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp", 0)
        jti = payload.get("jti")

        # Check if the token is blacklisted
        if is_token_blacklisted(jti):
            raise HTTPException(status_code=401, detail="Token has been revoked")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")  # Ensure this is raised correctly

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")  # General invalid token case

@app.post("/auth/logout")
def logout(token: str):
    """Blacklist a token upon user logout"""
    payload = decode_access_token(token)
    if payload:
        blacklist_access_token(payload["jti"])
        return {"message": "Successfully logged out"}
    raise HTTPException(status_code=400, detail="Invalid token")
