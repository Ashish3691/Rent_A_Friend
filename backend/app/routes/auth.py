from fastapi import APIRouter, HTTPException, status, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from models.user import User, UserCreate, UserLogin, Token, TokenRequest
from services.database import user_collection
from utils.security import get_password_hash, verify_password, create_access_token, decode_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

# ✅ Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["your_database_name"]
revoked_tokens_collection = db["revoked_tokens"]

# ✅ Ensure index for token expiration
revoked_tokens_collection.create_index("revoked_at", expireAfterSeconds=3600)

# 🔹 Utility function: Retrieve a user from the DB by email.
async def get_user_by_email(email: str):
    user = await user_collection.find_one({'email': email})
    if user:
        return User(**user)
    return None

# 🔹 Check if token is blacklisted
def is_token_blacklisted(jti: str) -> bool:
    return revoked_tokens_collection.find_one({"jti": jti}) is not None

# 🔹 Add token to the blacklist
def blacklist_access_token(jti: str):
    revoked_tokens_collection.insert_one({"jti": jti, "revoked_at": datetime.utcnow()})

@router.post("/signup", response_model=User)
async def signup(user_create: UserCreate):
    """Sign up a new user"""
    existing_user = await user_collection.find_one({'email': user_create.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user_create.dict()
    password = user_dict.pop("password")
    user_dict["hashed_password"] = get_password_hash(password)
    
    result = await user_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return User(**user_dict)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login a user and generate JWT token"""
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# 🔹 Get current user from JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    jti = payload.get("jti")
    if jti and is_token_blacklisted(jti):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")
    
    email: str = payload.get("sub")
    if not email:
        raise credentials_exception
    
    user = await get_user_by_email(email)
    if not user:
        raise credentials_exception
    
    return user

@router.post("/logout")
def logout(token_data: TokenRequest):
    token = token_data.token
    # Perform logout logic
    return {"message": "Successfully logged out"}