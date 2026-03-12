from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.product import (
    BrandCreate,
    BrandRead,
    BrandUpdate,
    ProductLineCreate,
    ProductLineRead,
    ProductLineUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate,
)
from src.schemas.tenant_product import TenantProductCreate, TenantProductRead, TenantProductUpdate
from src.crud import product as prod_crud
from src.crud import tenant_product as tp_crud
from src.utils.deps import get_current_user, require_role
from src.utils.pagination import PaginatedResponse, calculate_skip, calculate_total_pages
from src.models.user import User

router = APIRouter(prefix="/products", tags=["Products"])


# ---------------------------------------------------------------------------
# Brands
# ---------------------------------------------------------------------------

@router.get("/brands", response_model=PaginatedResponse[BrandRead])
def list_brands(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    skip = calculate_skip(page, page_size)
    items = prod_crud.get_brands(db, skip=skip, limit=page_size)
    total = prod_crud.count_brands(db)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post("/brands", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
def create_brand(
    data: BrandCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    return prod_crud.create_brand(db, data)


@router.patch("/brands/{brand_id}", response_model=BrandRead)
def update_brand(
    brand_id: str,
    data: BrandUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    brand = prod_crud.update_brand(db, brand_id, data)
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return brand


# ---------------------------------------------------------------------------
# Product Lines
# ---------------------------------------------------------------------------

@router.get("/lines", response_model=PaginatedResponse[ProductLineRead])
def list_product_lines(
    brand_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    skip = calculate_skip(page, page_size)
    items = prod_crud.get_product_lines_by_brand(db, brand_id, skip=skip, limit=page_size)
    total = prod_crud.count_product_lines_by_brand(db, brand_id)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post("/lines", response_model=ProductLineRead, status_code=status.HTTP_201_CREATED)
def create_product_line(
    data: ProductLineCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    return prod_crud.create_product_line(db, data)


@router.patch("/lines/{line_id}", response_model=ProductLineRead)
def update_product_line(
    line_id: str,
    data: ProductLineUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    line = prod_crud.update_product_line(db, line_id, data)
    if not line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product line not found"
        )
    return line


# ---------------------------------------------------------------------------
# Products (global catalog)
# ---------------------------------------------------------------------------

@router.get("/", response_model=PaginatedResponse[ProductRead])
def list_products(
    product_line_id: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    skip = calculate_skip(page, page_size)
    if product_line_id:
        items = prod_crud.get_products_by_line(db, product_line_id, skip=skip, limit=page_size)
        total = prod_crud.count_products_by_line(db, product_line_id)
    else:
        items = prod_crud.get_products(db, skip=skip, limit=page_size)
        total = prod_crud.count_products(db)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    return prod_crud.create_product(db, data)


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: str,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    product = prod_crud.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


# ---------------------------------------------------------------------------
# Tenant Products (salon-specific catalog)
# ---------------------------------------------------------------------------

@router.get("/tenant-catalog", response_model=PaginatedResponse[TenantProductRead])
def list_tenant_products(
    enabled_only: bool = False,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skip = calculate_skip(page, page_size)
    if enabled_only:
        items = tp_crud.get_enabled_tenant_products(db, current_user.tenant_id)
        total = tp_crud.count_enabled_tenant_products(db, current_user.tenant_id)
    else:
        items = tp_crud.get_tenant_products(db, current_user.tenant_id, skip=skip, limit=page_size)
        total = tp_crud.count_tenant_products(db, current_user.tenant_id)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post(
    "/tenant-catalog",
    response_model=TenantProductRead,
    status_code=status.HTTP_201_CREATED,
)
def add_product_to_catalog(
    data: TenantProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    data.tenant_id = current_user.tenant_id
    return tp_crud.create_tenant_product(db, data)


@router.patch("/tenant-catalog/{tp_id}", response_model=TenantProductRead)
def update_tenant_product(
    tp_id: str,
    data: TenantProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    tp = tp_crud.get_tenant_product(db, tp_id)
    if not tp or tp.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tenant product not found"
        )
    return tp_crud.update_tenant_product(db, tp_id, data)


@router.delete("/tenant-catalog/{tp_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tenant_product(
    tp_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    tp = tp_crud.get_tenant_product(db, tp_id)
    if not tp or tp.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tenant product not found"
        )
    tp_crud.delete_tenant_product(db, tp_id)

