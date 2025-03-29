from fastapi import FastAPI, Request, HTTPException, UploadFile, File, APIRouter
from routes import user, auth
from services.database import user_collection
from models.user import User, UserCreate, UserLogin
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uuid
import shutil
from utils.security import get_password_hash, pwd_context, create_access_token

app = FastAPI()

router = APIRouter()

@app.post("/register")
async def register_user(user: UserCreate, profile_picture: UploadFile = File(...)):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    profile_pic_filename = f"profile_picture/{uuid.uuid4()}_{profile_picture.filename}"
    with open(profile_pic_filename, "wb") as buffer:
        shutil.copyfileobj(profile_picture.file, buffer)
    
    hashed_password = pwd_context.hash(user.password)
    new_user = {"name": user.name, 
                "email": user.email, 
                "password": hashed_password, 
                "user_role": user.user_role,
                "height": user.height,
                "eye": user.eye,
                "age": user.age,
                "hair": user.hair,
                "city": user.city,
                "state": user.state,
                "phone_number": user.phone_number,
                "profile_picture": profile_pic_filename
                
                
}
    
    result = await user_collection.insert_one(new_user)
    
    # access_token = create_access_token({"sub": user["email"], "role": user["user_role"]})
    return {"message": "User registered successfully", 
            "user_id": str(result.inserted_id)
            }