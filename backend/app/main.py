 # Entry point to start the FastAPI server
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form, Depends
from routes import user, auth
from services.database import user_collection
from models.user import User, UserCreate, UserLogin
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uuid
import shutil
from utils.security import get_password_hash, pwd_context, create_access_token
from jose import jwt
from config import SECRET_KEY, ALGORITHM



app = FastAPI(title="deaRent A Friend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

templates = Jinja2Templates(directory="templates")

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/authentication", tags=["Authentication"])



@app.get("/")
async def read_root():
    return {"message": "Welcome to this Platform"}

        
@app.get("/signup", response_class=HTMLResponse)
async def serve_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def serve_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/register")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    user_role: str = Form(...),
    height: float = Form(...),
    eye: str = Form(...),
    age: int = Form(...),
    hair: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    phone_number: str = Form(...),
    profile_picture: UploadFile = File(...)
):
    # Check if email already exists
    existing_user = await user_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    print("✅ Email check passed")

    # Save the uploaded profile picture
    profile_pic_filename = f"{uuid.uuid4()}_{profile_picture.filename}"
    with open(profile_pic_filename, "wb") as buffer:
        shutil.copyfileobj(profile_picture.file, buffer)

    print("✅ Image saved successfully:", profile_pic_filename)

    # Hash password
    hashed_password = pwd_context.hash(password)

    # Create user dictionary
    new_user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "user_role": user_role,
        "height": height,
        "eye": eye,
        "age": age,
        "hair": hair,
        "city": city,
        "state": state,
        "phone_number": phone_number,
        "profile_picture": profile_pic_filename,  # ✅ Save only the file path, not the file itself
    }

    print("✅ User data created successfully")

    # Insert into MongoDB
    result = await user_collection.insert_one(new_user)

    print("✅ User saved to database")

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }



@app.post("/login")
async def login_user(login: UserLogin):
    user = await user_collection.find_one({"email": login.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not pwd_context.verify(login.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": user["email"], "role": user["user_role"]})
    return {"message": "Login successful", 
            "user_id": str(user["_id"])
            }
    
@app.put("/update_profile")
async def update_profile(token: str = Depends(oauth2_scheme), profile_picture: UploadFile = None, update_user: UserCreate = None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        user = await user_collection.find_one({"email": user_email})

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        update_data = {}

        if update_user.name:
            update_data["name"] = update_user.name
        if update_user.email:
            existing_email = await user_collection.find_one({"email": update_user.email})
            if existing_email:
                raise HTTPException(status_code=400, detail="Email already in use")
            update_data["email"] = update_user.email
        if update_user.password:
            update_data["password"] = pwd_context.hash(update_user.password)
        if profile_picture:
            profile_pic_filename = f"profile_pictures/{uuid.uuid4()}_{profile_picture.filename}"
            with open(profile_pic_filename, "wb") as buffer:
                shutil.copyfileobj(profile_picture.file, buffer)
            update_data["profile_picture"] = profile_pic_filename

        await user_collection.update_one({"email": user_email}, {"$set": update_data})
        return {"message": "Profile updated successfully"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    
    
    
    
    
    
    
    
    
    


