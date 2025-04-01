import pytest
from fastapi.testclient import TestClient
from app.utils.security import app, create_access_token, blacklist_access_token, decode_access_token
from datetime import timedelta
from fastapi import HTTPException

client = TestClient(app)

def test_create_access_token():
    """Test if JWT access token is generated correctly"""
    token = create_access_token({"sub": "test_user"})
    assert isinstance(token, str)

def test_decode_valid_token():
    """Test if a valid JWT token can be decoded"""
    token = create_access_token({"sub": "test_user"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == "test_user"

def test_blacklist_token():
    """Test if a token can be blacklisted and rejected upon decoding"""
    token = create_access_token({"sub": "test_user"})
    payload = decode_access_token(token)
    jti = payload.get("jti")
    
    if jti:
        blacklist_access_token(jti)

        with pytest.raises(HTTPException) as e:
            decode_access_token(token)
        assert e.value.status_code == 401
        assert "Token has been revoked" in e.value.detail

def test_logout():
    """Test if logging out blacklists a token"""
    token = create_access_token({"sub": "test_user"})

    # Send token as a query parameter instead of JSON body
    response = client.post(f"/auth/logout?token={token}")

    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Successfully logged out"}

    # Ensure token is blacklisted
    with pytest.raises(Exception) as e:
        decode_access_token(token)

    assert "Token has been revoked" in str(e.value)

