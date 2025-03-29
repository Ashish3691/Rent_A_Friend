from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URI, DATABASE_NAME

client = AsyncIOMotorClient(MONGODB_URI)


database = client["rent_a_friend_user"]  # Access database dynamically
user_collection = database.get_collection("UserData")  # Corrected collection reference
