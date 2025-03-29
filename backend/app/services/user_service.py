# User-specific business logic

# from models.user import User
# from config import MONGODB_URI, DATABASE_NAME
# from pymongo import MongoClient
# from bson.objectid import ObjectId

# client = MongoClient(MONGODB_URI)
# db = client[DATABASE_NAME]
# user_collection = db["UserData"]

# def create_user(user: User):
#     user_dict = user.dict(by_alias=True)
#     result = user_collection.insert_one(user_dict)
#     user_dict['id'] = str(result.inserted_id)
#     return user_dict

# def get_user(user_id: str):
#     user_data = user_collection.find_one({'_id': ObjectId(user_id)})
#     if user_data:
#         user_data["_id"] = str(user_data['_id'])
#     return user_data


from bson.objectid import ObjectId
from models.user import User
from services.database import user_collection  # Import the shared async connection

async def create_user(user: User):
    user_dict = user.dict(by_alias=True)
    result = await user_collection.insert_one(user_dict)  # Use async insert
    user_dict['id'] = str(result.inserted_id)
    return user_dict

async def get_user(user_id: str):
    user_data = await user_collection.find_one({'_id': ObjectId(user_id)})  # Use async find
    if user_data:
        user_data["_id"] = str(user_data['_id'])
    return user_data
