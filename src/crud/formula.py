from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.models.formula import Formula, FormulaItem
from src.models.inventory import InventoryItem, InventoryTxn
from src.models.tenant_product import TenantProduct
from src.schemas.formula import FormulaCreate, FormulaUpdate


class InsufficientInventoryError(Exception):
    """Raised when there is insufficient inventory to create a formula."""
    def __init__(self, insufficient_items: list[dict]):
        self.insufficient_items = insufficient_items
        super().__init__(f"Insufficient inventory: {len(insufficient_items)} item(s)")


def get_formula(db: Session, formula_id: str) -> Formula | None:
    return (
        db.query(Formula)
        .options(joinedload(Formula.formula_items))
        .filter(Formula.id == formula_id)
        .first()
    )


def get_formulas_by_customer(
    db: Session, tenant_id: str, customer_id: str, skip: int = 0, limit: int = 50
) -> list[Formula]:
    return (
        db.query(Formula)
        .options(joinedload(Formula.formula_items))
        .filter(Formula.tenant_id == tenant_id, Formula.customer_id == customer_id)
        .order_by(Formula.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_formulas_by_tenant(
    db: Session, tenant_id: str, skip: int = 0, limit: int = 100
) -> list[Formula]:
    return (
        db.query(Formula)
        .filter(Formula.tenant_id == tenant_id)
        .order_by(Formula.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_formula(db: Session, data: FormulaCreate) -> Formula:
    """
    Create a formula with its items and automatically:
    1. Validate sufficient inventory for all items
    2. Record inventory CONSUME transactions for each product used.
    3. Deduct stock from inventory_items.
    
    Raises InsufficientInventoryError if insufficient inventory.
    """
    # First, validate all inventory items have sufficient stock
    insufficient_items = []
    for item_data in data.items:
        # Get tenant product info for better error messages
        tenant_product = (
            db.query(TenantProduct)
            .options(joinedload(TenantProduct.product))
            .filter(TenantProduct.id == item_data.tenant_product_id)
            .first()
        )
        if tenant_product:
            product_name = tenant_product.custom_name or (
                tenant_product.product.name if tenant_product.product else "Unknown Product"
            )
            tracking_unit = tenant_product.tracking_unit
        else:
            product_name = "Unknown Product"
            tracking_unit = "units"
        
        inv_item = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.location_id == data.location_id,
                InventoryItem.tenant_product_id == item_data.tenant_product_id,
            )
            .first()
        )
        if not inv_item:
            insufficient_items.append({
                "tenant_product_id": item_data.tenant_product_id,
                "product_name": product_name,
                "tracking_unit": tracking_unit,
                "amount_needed": item_data.amount_used,
                "available": 0.0,
                "reason": "Inventory item not found for this location"
            })
        else:
            available = float(inv_item.on_hand_qty)
            needed = item_data.amount_used
            if available < needed:
                insufficient_items.append({
                    "tenant_product_id": item_data.tenant_product_id,
                    "product_name": product_name,
                    "tracking_unit": tracking_unit,
                    "amount_needed": needed,
                    "available": available,
                    "reason": f"Insufficient inventory. Need {needed} {tracking_unit}, have {available} {tracking_unit}"
                })
    
    if insufficient_items:
        raise InsufficientInventoryError(insufficient_items)
    
    # All validations passed, proceed with creation
    formula_data = data.model_dump(exclude={"items"})
    formula = Formula(**formula_data)
    db.add(formula)
    db.flush()  # Get formula.id before adding items

    for item_data in data.items:
        formula_item = FormulaItem(
            formula_id=formula.id,
            tenant_product_id=item_data.tenant_product_id,
            amount_used=item_data.amount_used,
            cost_at_time=item_data.cost_at_time,
        )
        db.add(formula_item)

        # Deduct inventory at the formula's location
        inv_item = (
            db.query(InventoryItem)
            .filter(
                InventoryItem.location_id == data.location_id,
                InventoryItem.tenant_product_id == item_data.tenant_product_id,
            )
            .first()
        )
        if inv_item:
            inv_item.on_hand_qty = float(inv_item.on_hand_qty) - item_data.amount_used
            txn = InventoryTxn(
                tenant_id=data.tenant_id,
                inventory_item_id=inv_item.id,
                formula_id=formula.id,
                user_id=data.created_by_user_id,
                txn_type="CONSUME",
                qty_delta=-item_data.amount_used,
                unit_cost_at_time=item_data.cost_at_time,
            )
            db.add(txn)

    db.commit()
    db.refresh(formula)
    return formula


def update_formula(db: Session, formula_id: str, data: FormulaUpdate) -> Formula | None:
    formula = db.query(Formula).filter(Formula.id == formula_id).first()
    if not formula:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(formula, field, value)
    db.commit()
    db.refresh(formula)
    return formula


def delete_formula(db: Session, formula_id: str) -> bool:
    formula = db.query(Formula).filter(Formula.id == formula_id).first()
    if not formula:
        return False
    db.delete(formula)
    db.commit()
    return True


def count_formulas_by_customer(db: Session, tenant_id: str, customer_id: str) -> int:
    return (
        db.query(func.count(Formula.id))
        .filter(Formula.tenant_id == tenant_id, Formula.customer_id == customer_id)
        .scalar() or 0
    )


def count_formulas_by_tenant(db: Session, tenant_id: str) -> int:
    return (
        db.query(func.count(Formula.id))
        .filter(Formula.tenant_id == tenant_id)
        .scalar() or 0
    )

