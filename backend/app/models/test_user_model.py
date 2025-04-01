import pytest
from pydantic import ValidationError
from app.models.user import UserCreate, UserModel

def test_valid_user_creation():
    user = UserCreate(
        name="John Doe",
        email="johndoe@example.com",
        password="SecurePass123",
        user_role="user",
        height=175,
        age=30,
        eye="blue",
        hair="black",
        city="New York",
        state="NY",
        phone_number=1234567890,
        profile_picture=None
    )
    assert user.name == "John Doe"
    assert user.email == "johndoe@example.com"
    assert user.age == 30


def test_invalid_phone_number():
    with pytest.raises(ValidationError):
        UserCreate(
            name="Jane Doe",
            email="janedoe@example.com",
            password="StrongPass!",
            user_role="user",
            height=165,
            age=25,
            eye="green",
            hair="blonde",
            city="Los Angeles",
            state="CA",
            phone_number=123,
            profile_picture=None
        )


def test_invalid_age():
    with pytest.raises(ValidationError):
        UserModel(
            profile_pic="some_url",
            body_type="slim",
            age=-5,
            user_role="user",
            city="Chicago",
            state="IL",
            verification_doc=None,
            phone_number=9876543210,
            height="170cm",
            eye="brown",
            hair="black",
            type="user"
        )

def test_missing_email():
    with pytest.raises(ValidationError):
        UserCreate(
            name="Test User",
            password="TestPass123",
            user_role="user",
            height=180,
            age=28,
            eye="hazel",
            hair="brown",
            city="Houston",
            state="TX",
            phone_number=1234567890,
            profile_picture=None
        )
