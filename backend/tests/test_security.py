import unittest
from datetime import timedelta
from fastapi import HTTPException
from app.utils.security import get_password_hash, verify_password, create_access_token, decode_access_token

class TestSecurity(unittest.TestCase):
    
    def test_password_hashing(self):
        password = "securepassword123"
        hashed = get_password_hash(password)
        self.assertTrue(verify_password(password, hashed))
        
    def test_token_creation_and_decoding(self):
        data = {"sub": "test_user"}
        token = create_access_token(data, timedelta(minutes=5))
        decoded = decode_access_token(token)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["sub"], "test_user")
        
    def test_expire_token(self):
        data = {"sub": "test_user"}
        token = create_access_token(data, timedelta(seconds=-1))  # Expired token

        with self.assertRaises(HTTPException) as context:
            decode_access_token(token)

        self.assertEqual(context.exception.status_code, 401)
        self.assertIn("expired", context.exception.detail.lower())  # More flexible error message check

if __name__ == "__main__":
    unittest.main()