from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# FormulaItem
# ---------------------------------------------------------------------------

class FormulaItemBase(BaseModel):
    tenant_product_id: str
    amount_used: float
    cost_at_time: float | None = None


class FormulaItemCreate(FormulaItemBase):
    pass


class FormulaItemRead(FormulaItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    formula_id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Formula
# ---------------------------------------------------------------------------

class FormulaBase(BaseModel):
    formula_name: str | None = None
    service_type: str | None = None
    notes: str | None = None


class FormulaCreate(FormulaBase):
    tenant_id: str
    location_id: str
    customer_id: str
    created_by_user_id: str
    items: list[FormulaItemCreate] = []


class FormulaUpdate(BaseModel):
    formula_name: str | None = None
    service_type: str | None = None
    notes: str | None = None


class FormulaRead(FormulaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    location_id: str
    customer_id: str
    created_by_user_id: str
    created_at: datetime
    formula_items: list[FormulaItemRead] = []





