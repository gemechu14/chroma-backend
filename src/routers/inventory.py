from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemRead,
    InventoryItemUpdate,
    InventoryTxnCreate,
    InventoryTxnRead,
)
from src.crud import inventory as crud
from src.utils.deps import get_current_user, require_role
from src.utils.pagination import PaginatedResponse, calculate_skip, calculate_total_pages
from src.models.user import User

router = APIRouter(prefix="/inventory", tags=["Inventory"])


# ---------------------------------------------------------------------------
# Inventory Items
# ---------------------------------------------------------------------------

@router.get("/items", response_model=list[InventoryItemRead])
def list_inventory(
    location_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_inventory_by_location(db, current_user.tenant_id, location_id)


@router.get("/items/low-stock", response_model=list[InventoryItemRead])
def low_stock_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_low_stock_items(db, current_user.tenant_id)


@router.post(
    "/items", response_model=InventoryItemRead, status_code=status.HTTP_201_CREATED
)
def create_inventory_item(
    data: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    data.tenant_id = current_user.tenant_id
    existing = crud.get_inventory_item_by_location_product(
        db, data.location_id, data.tenant_product_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Inventory item already exists for this location and product",
        )
    return crud.create_inventory_item(db, data)


@router.get("/items/{item_id}", response_model=InventoryItemRead)
def get_inventory_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = crud.get_inventory_item(db, item_id)
    if not item or item.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found"
        )
    return item


@router.patch("/items/{item_id}", response_model=InventoryItemRead)
def update_inventory_item(
    item_id: str,
    data: InventoryItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    item = crud.get_inventory_item(db, item_id)
    if not item or item.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found"
        )
    return crud.update_inventory_item(db, item_id, data)


# ---------------------------------------------------------------------------
# Inventory Transactions
# ---------------------------------------------------------------------------

@router.get("/transactions", response_model=PaginatedResponse[InventoryTxnRead])
def list_transactions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skip = calculate_skip(page, page_size)
    items = crud.get_txns_by_tenant(db, current_user.tenant_id, skip=skip, limit=page_size)
    total = crud.count_txns_by_tenant(db, current_user.tenant_id)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.get("/transactions/{item_id}", response_model=PaginatedResponse[InventoryTxnRead])
def list_item_transactions(
    item_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = crud.get_inventory_item(db, item_id)
    if not item or item.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found"
        )
    skip = calculate_skip(page, page_size)
    items = crud.get_txns_by_inventory_item(db, item_id, skip=skip, limit=page_size)
    total = crud.count_txns_by_inventory_item(db, item_id)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post(
    "/transactions",
    response_model=InventoryTxnRead,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    data: InventoryTxnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    data.tenant_id = current_user.tenant_id
    data.user_id = current_user.id
    item = crud.get_inventory_item(db, data.inventory_item_id)
    if not item or item.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found"
        )
    return crud.create_inventory_txn(db, data)

