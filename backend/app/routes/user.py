# from fastapi import APIRouter, HTTPException
# from models.user import User
# from services import user_service

# router = APIRouter()

# @router.post('/', response_model=User)
# def create_user(user:User):
#     created_user = user_service.create_user(user)
#     return created_user

# @router.get("/{user_id}", response_model=User)
# def get_user(user_id: str):
#     user_data = user_service.get_user(user_id)
#     if user_data:
#         return user_data
#     raise HTTPException(status_code=404, detail="User not found")

from fastapi import APIRouter, HTTPException
from models.user import User
from services.user_service import create_user, get_user

router = APIRouter()

@router.post("/register")
async def register_user(user: User):
    user_data = await create_user(user)
    return user_data

@router.get("/{user_id}")
async def fetch_user(user_id: str):
    user_data = await get_user(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data
