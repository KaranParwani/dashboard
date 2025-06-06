from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from patient.services.database import db_manager
from patient.services.password_encrypt import PasswordProcessor

from config import SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD, SALT


def add_super_admin():
    """

    :return: None.
    """
    session = db_manager.get_session()  # Get a session
    try:
        Users = db_manager.get_class("users")
        # Check if super_admin already exists
        existing_admin = (
            session.query(Users).filter_by(user_type="admin", active=True).first()
        )
        if not existing_admin:
            hashed_password = PasswordProcessor.encrypt_password(
                SUPER_ADMIN_PASSWORD, SALT.encode("utf-8")
            )
            super_admin = Users(
                user_email=SUPER_ADMIN_EMAIL,
                user_password=hashed_password,
                user_type="admin",
            )
            session.add(super_admin)
            session.commit()
            print("Super admin created successfully.")
        else:
            print("Super admin already exists.")

    except Exception as e:
        print(e)
        session.rollback()


class AdminAuthenticator:
    """Handles admin authentication."""

    def __init__(self, session, secret_key, algorithm):
        """

        :param session:
        :param secret_key:
        :param algorithm:
        """
        self.session = session
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.security = HTTPBearer()  # Token extraction

    def authenticate(self, email: str, password: str):
        """Authenticate admin with email and password."""
        Users = db_manager.get_class("users")
        if not Users:
            raise RuntimeError(
                "Users class not found. Ensure database is correctly mapped."
            )

        # Query admin user
        user = (
            self.session.query(Users)
            .filter_by(user_email=email, user_type="admin")
            .first()
        )
        if user and PasswordProcessor.verify_password(password, user.user_password):
            return user
        return None

    def __decode_token(self, token: str) -> dict:
        """Decode the JWT token."""
        try:
            return jwt.decode(token, self.secret_key, algorithms=self.algorithm)
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Invalid token.") from e

    def authenticate_admin_token(self, authorization):
        """
        Authenticate and validate the access token. Ensure the user is an admin.

        :param authorization: HTTP Authorization Credentials containing the token.
        :return: Decoded token payload if valid and user is admin.
        """
        token = authorization.split("Bearer ")[1]

        try:
            # Decode the token
            payload = self.__decode_token(token)

            # Check token type
            if payload.get("type") != "access":
                raise HTTPException(status_code=403, detail="Invalid token type.")

            # Check user type
            if payload.get("user_type") != "admin":
                raise HTTPException(
                    status_code=403, detail="Unauthorized: Admin access required."
                )

            # Check expiration
            if datetime.utcnow().timestamp() > payload.get("exp", 0):
                raise HTTPException(status_code=401, detail="Token has expired.")

            return payload  # Return decoded payload for further use if necessary

        except JWTError as e:
            raise HTTPException(status_code=401, detail="Invalid token.") from e
