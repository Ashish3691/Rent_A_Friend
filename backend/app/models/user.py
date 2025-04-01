# # Example user model/schema
# from pydantic import BaseModel, Field, EmailStr
# from typing import Optional, Literal, Union
# from datetime import datetime




# # Main User model stored in the database
# class User(BaseModel):
#     id: Optional[str] = Field(None, alias="_id")
#     name: str
#     email: EmailStr
#     profile_picture: Optional[str] = None  # IMG URL or base64 encoded image
#     hashed_password: str
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     active: bool = True
#     user_role: Literal['user', 'rep']
    

#     class Config:
#         populate_by_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {datetime: lambda dt: dt.isoformat()}

# # Model used during signup (plaintext password is received and then hashed)
# class UserCreate(BaseModel):
#     name: str
#     email: EmailStr
#     password: str
#     user_role: Literal['user', 'rep'] 
#     height: int
#     age: int
#     eye: str
#     hair: str
#     city: str
#     state: str
#     phone_number: int
#     profile_picture: str
    
    
# class UserSpec(BaseModel):
#     profile_pic: str
#     body_type: str
#     age: int
#     user_role: str
#     city: str
#     state: str
#     #optional
#     verification_doc: str # Thinking
#     phone_number: int
 
    
    
# class user(UserSpec):
#     profile_pic: str
#     height: str
#     eye: str
#     hair: str
#     body_type: str
#     age: int
#     type: Literal['user']
#     user_role: str
#     city: str
#     state: str
#     #optional
#     verification_doc: str # Thinking
#     phone_number: int
    
# class rep(UserSpec):
#     price: int
#     profile_pic: str
#     height: str
#     eye: str
#     hair: str
#     type: Literal['rep']
#     body_type: str
#     age: int
#     user_role: str
#     city: str
#     state: str
#     #optional
#     verification_doc: str # Thinking
#     phone_number: int
    
# class LargeData(BaseModel):
#     language: list
#     more_info: list
#     activities: list
    
# class Status(BaseModel):
#     active: bool
    



# # Model for login requests
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# # Models for token response and data extraction
# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     email: Optional[str] = None

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional, Literal, List
from datetime import datetime

# Main User model stored in the database
class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    profile_picture: Optional[str] = None  # IMG URL or base64 encoded image
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True
    user_role: Literal['user', 'rep']

    # class Config:
    #     populate_by_name = True
    #     arbitrary_types_allowed = True
    #     json_encoders = {datetime: lambda dt: dt.isoformat()}
    

    
           
    
    model_config = ConfigDict(from_attributes = True )


    

# Model used during signup (plaintext password is received and then hashed)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_role: Literal['user', 'rep']
    height: int
    age: int
    eye: str
    hair: str
    city: str
    state: str
    phone_number: int
    profile_picture: Optional[str] = None

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if len(str(v)) not in [10, 12]:
            raise ValueError("Invalid phone number format")
        return v

class UserSpec(BaseModel):
    profile_pic: str
    body_type: str
    age: int
    user_role: str
    city: str
    state: str
    verification_doc: Optional[str] = None
    phone_number: int

class UserType(UserSpec):
    height: str
    eye: str
    hair: str
    type: Literal['user', 'rep']

class UserModel(UserType):
    price: Optional[int] = None
    
    @field_validator("age")
    def validate_age(cls, v):
        if v <= 0:
            raise ValueError("Age must be a positive number")
        return v

class LargeData(BaseModel):
    language: List[str]
    more_info: List[str]
    activities: List[str]

class Status(BaseModel):
    active: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    
class TokenRequest(BaseModel):
    token: str
