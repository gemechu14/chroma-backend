from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str = "EMPLOYEE"
    is_active: bool = True
    default_location_id: str | None = None


class UserCreate(UserBase):
    tenant_id: str
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None
    default_location_id: str | None = None
    password: str | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    last_login_at: datetime | None = None
    created_at: datetime


# Returned after successful login
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: str | None = None
    tenant_id: str | None = None

