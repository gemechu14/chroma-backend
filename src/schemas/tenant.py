from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, EmailStr

if TYPE_CHECKING:
    from src.schemas.user import UserRead


# ---------------------------------------------------------------------------
# Tenant
# ---------------------------------------------------------------------------

class TenantBase(BaseModel):
    name: str
    plan: str | None = None
    status: str = "trial"


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None
    plan: str | None = None
    status: str | None = None


class TenantRead(TenantBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------------

class LocationBase(BaseModel):
    name: str
    address: str | None = None
    timezone: str | None = None


class LocationCreate(LocationBase):
    tenant_id: str


class LocationUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    timezone: str | None = None


class LocationRead(LocationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Tenant Registration
# ---------------------------------------------------------------------------

class TenantRegistration(BaseModel):
    """Schema for tenant registration."""
    tenant_name: str
    plan: str | None = None
    
    # Admin user details
    admin_email: EmailStr
    admin_password: str
    admin_full_name: str
    
    # Default location
    location_name: str
    location_address: str | None = None
    location_timezone: str | None = None


class TenantRegistrationResponse(BaseModel):
    """Response after successful tenant registration."""
    tenant: TenantRead
    location: LocationRead
    admin_user_id: str
    admin_email: EmailStr
    message: str = "Tenant registered successfully. You can now login with your admin credentials."


