from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# InventoryItem
# ---------------------------------------------------------------------------

class InventoryItemBase(BaseModel):
    on_hand_qty: float = 0.0
    reorder_level_qty: float | None = None


class InventoryItemCreate(InventoryItemBase):
    tenant_id: str
    location_id: str
    tenant_product_id: str


class InventoryItemUpdate(BaseModel):
    on_hand_qty: float | None = None
    reorder_level_qty: float | None = None


class InventoryItemRead(InventoryItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    location_id: str
    tenant_product_id: str
    updated_at: datetime
    created_at: datetime


# ---------------------------------------------------------------------------
# InventoryTxn
# ---------------------------------------------------------------------------

class InventoryTxnBase(BaseModel):
    txn_type: str
    qty_delta: float
    unit_cost_at_time: float | None = None
    note: str | None = None


class InventoryTxnCreate(InventoryTxnBase):
    tenant_id: str
    inventory_item_id: str
    user_id: str
    formula_id: str | None = None


class InventoryTxnRead(InventoryTxnBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    inventory_item_id: str
    user_id: str
    formula_id: str | None = None
    created_at: datetime





