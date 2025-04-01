import unittest
from datetime import timedelta
from app.utils.security import create_access_token, decode_access_token, blacklist_access_token
from fastapi import FastAPI, HTTPException


class TestTokenBlacklist(unittest.TestCase):

    def test_blacklist_token(self):
        data = {"sub": "test_user"}
        token = create_access_token(data, timedelta(minutes=5))
        
        payload = decode_access_token(token)
        self.assertIsNotNone(payload)

        # Blacklist the jti, NOT the full token
        blacklist_access_token(payload["jti"])

        # Ensure that the token is now invalid
        with self.assertRaises(HTTPException) as context:
            decode_access_token(token)

        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token has been revoked")
        
    

if __name__ == "__main__":
    unittest.main()
