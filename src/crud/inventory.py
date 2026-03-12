from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.inventory import InventoryItem, InventoryTxn
from src.schemas.inventory import InventoryItemCreate, InventoryItemUpdate, InventoryTxnCreate


# ---------------------------------------------------------------------------
# InventoryItem
# ---------------------------------------------------------------------------

def get_inventory_item(db: Session, item_id: str) -> InventoryItem | None:
    return db.query(InventoryItem).filter(InventoryItem.id == item_id).first()


def get_inventory_item_by_location_product(
    db: Session, location_id: str, tenant_product_id: str
) -> InventoryItem | None:
    return (
        db.query(InventoryItem)
        .filter(
            InventoryItem.location_id == location_id,
            InventoryItem.tenant_product_id == tenant_product_id,
        )
        .first()
    )


def get_inventory_by_location(
    db: Session, tenant_id: str, location_id: str, skip: int = 0, limit: int = 200
) -> list[InventoryItem]:
    return (
        db.query(InventoryItem)
        .filter(
            InventoryItem.tenant_id == tenant_id,
            InventoryItem.location_id == location_id,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_low_stock_items(db: Session, tenant_id: str) -> list[InventoryItem]:
    """Return items where on_hand_qty <= reorder_level_qty."""
    return (
        db.query(InventoryItem)
        .filter(
            InventoryItem.tenant_id == tenant_id,
            InventoryItem.reorder_level_qty.isnot(None),
            InventoryItem.on_hand_qty <= InventoryItem.reorder_level_qty,
        )
        .all()
    )


def create_inventory_item(db: Session, data: InventoryItemCreate) -> InventoryItem:
    item = InventoryItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_inventory_item(
    db: Session, item_id: str, data: InventoryItemUpdate
) -> InventoryItem | None:
    item = get_inventory_item(db, item_id)
    if not item:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


# ---------------------------------------------------------------------------
# InventoryTxn
# ---------------------------------------------------------------------------

def create_inventory_txn(db: Session, data: InventoryTxnCreate) -> InventoryTxn:
    txn = InventoryTxn(**data.model_dump())
    db.add(txn)
    # Apply qty_delta to the parent inventory item
    item = get_inventory_item(db, data.inventory_item_id)
    if item:
        item.on_hand_qty = float(item.on_hand_qty) + data.qty_delta
    db.commit()
    db.refresh(txn)
    return txn


def get_txns_by_inventory_item(
    db: Session, inventory_item_id: str, skip: int = 0, limit: int = 100
) -> list[InventoryTxn]:
    return (
        db.query(InventoryTxn)
        .filter(InventoryTxn.inventory_item_id == inventory_item_id)
        .order_by(InventoryTxn.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_txns_by_tenant(
    db: Session, tenant_id: str, skip: int = 0, limit: int = 100
) -> list[InventoryTxn]:
    return (
        db.query(InventoryTxn)
        .filter(InventoryTxn.tenant_id == tenant_id)
        .order_by(InventoryTxn.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_txns_by_tenant(db: Session, tenant_id: str) -> int:
    return (
        db.query(func.count(InventoryTxn.id))
        .filter(InventoryTxn.tenant_id == tenant_id)
        .scalar() or 0
    )


def count_txns_by_inventory_item(db: Session, inventory_item_id: str) -> int:
    return (
        db.query(func.count(InventoryTxn.id))
        .filter(InventoryTxn.inventory_item_id == inventory_item_id)
        .scalar() or 0
    )

