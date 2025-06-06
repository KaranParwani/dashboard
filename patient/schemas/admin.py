from pydantic import BaseModel, EmailStr


class AdminLogin(BaseModel):
    user_email: EmailStr
    password: str
