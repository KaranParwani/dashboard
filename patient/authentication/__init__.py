from jose import jwt
from datetime import timedelta, datetime

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRY, REFRESH_TOKEN_EXPIRY


class TokenManager:
    """Handles the creation of JWT tokens."""

    @staticmethod
    def create_token(data: dict, expires_delta: timedelta, token_type: str):
        """Create a JWT token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire, "type": token_type})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    def create_access_token(cls, data: dict):
        """Create an access token."""
        return cls.create_token(data, timedelta(minutes=int(ACCESS_TOKEN_EXPIRY)), "access")

    @classmethod
    def create_refresh_token(cls, data: dict):
        """Create a refresh token."""
        return cls.create_token(data, timedelta(days=int(REFRESH_TOKEN_EXPIRY)), "refresh")
