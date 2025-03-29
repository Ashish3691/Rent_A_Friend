# Example route (authentication, etc.)

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from bson.objectid import ObjectId
from models.user import User, UserCreate, UserLogin, Token, TokenData
from services.database import user_collection
from utils.security import get_password_hash, verify_password, create_access_token, decode_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

# Utility function: Retrieve a user from the DB by email.
async def get_user_by_email(email: str):
    user = await user_collection.find_one({'email': email})
    if user:
        return User(**user)
    return None

@router.post("/signup", response_model=User)
async def signup(user_create: UserCreate):
    # Check if the email is already registered.
    existing_user = await user_collection.find_one({'email': user_create.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Prepare the user document.
    user_dict = user_create.dict()
    password = user_dict.pop("password")
    user_dict["hashed_password"] = get_password_hash(password)
    
    # Insert user into the MongoDB collection.
    result = await user_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return User(**user_dict)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Here, the form uses "username" field to send the email.
    user = await get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# Dependency to get the current user based on JWT token.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception                         
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = await get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user