from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TenantProductBase(BaseModel):
    custom_name: str | None = None
    is_enabled: bool = True
    tracking_unit: str = "G"
    default_unit_cost: float | None = None
    currency: str | None = None


class TenantProductCreate(TenantProductBase):
    tenant_id: str
    product_id: str


class TenantProductUpdate(BaseModel):
    custom_name: str | None = None
    is_enabled: bool | None = None
    tracking_unit: str | None = None
    default_unit_cost: float | None = None
    currency: str | None = None


class TenantProductRead(TenantProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    product_id: str
    created_at: datetime


