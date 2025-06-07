from starlette import status
from fastapi import APIRouter, HTTPException

from config import SECRET_KEY, ALGORITHM
from patient.authentication import TokenManager
from patient.schemas.admin import AdminLogin
from patient.services.admin import AdminAuthenticator
from patient.services.database import db_manager


admin_router = APIRouter()


@admin_router.post("/login")
def admin_login(credentials: AdminLogin):
    """Admin login endpoint."""
    session = db_manager.get_session()
    credentials = credentials.model_dump()
    try:
        # Authenticate user
        authenticator = AdminAuthenticator(session, SECRET_KEY, ALGORITHM)
        user = authenticator.authenticate(
            credentials.get("user_email"), credentials.get("password")
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # Generate tokens
        access_token = TokenManager.create_access_token(
            data={
                "sub": user.user_email,
                "user_type": user.user_type,
                "user_id": user.user_id,
            }
        )
        refresh_token = TokenManager.create_refresh_token(
            data={
                "sub": user.user_email,
                "user_type": user.user_type,
                "user_id": user.user_id,
            }
        )

        return {
            "username": credentials.get("user_email"),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    finally:
        session.close()
