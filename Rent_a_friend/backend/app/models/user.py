# Example user model/schema


from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    profile_picture: Optional[str] = None  # IMG URL or base64 encoded image
    name: str
    age: int
    city: str
    state: str
    country: str
    active: bool = True  # Active or not (binary)
    # Options for physical appearance and attributes
    eyes: Optional[str] = None   # Options can be enforced in frontend
    hair: Optional[str] = None   # Options can be enforced in frontend
    body_type: Optional[str] = None   # Options
    ethnicity: Optional[str] = None   # Options
    languages: Optional[str] = None   # Options (or use a list if needed)
    more_info: Optional[str] = None   # More information about the user (paragraph)
    activities: Optional[str] = None  # Activities I'm available for (paragraph or options)