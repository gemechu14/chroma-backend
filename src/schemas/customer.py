from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    full_name: str
    phone: str | None = None
    email: str | None = None
    notes: str | None = None
    home_location_id: str | None = None


class CustomerCreate(CustomerBase):
    tenant_id: str


class CustomerUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    notes: str | None = None
    home_location_id: str | None = None


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    created_at: datetime





