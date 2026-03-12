from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.tenant_product import TenantProduct
from src.schemas.tenant_product import TenantProductCreate, TenantProductUpdate


def get_tenant_product(db: Session, tenant_product_id: str) -> TenantProduct | None:
    return (
        db.query(TenantProduct)
        .filter(TenantProduct.id == tenant_product_id)
        .first()
    )


def get_tenant_products(
    db: Session, tenant_id: str, skip: int = 0, limit: int = 200
) -> list[TenantProduct]:
    return (
        db.query(TenantProduct)
        .filter(TenantProduct.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_enabled_tenant_products(
    db: Session, tenant_id: str
) -> list[TenantProduct]:
    return (
        db.query(TenantProduct)
        .filter(TenantProduct.tenant_id == tenant_id, TenantProduct.is_enabled == True)  # noqa: E712
        .all()
    )


def create_tenant_product(db: Session, data: TenantProductCreate) -> TenantProduct:
    tp = TenantProduct(**data.model_dump())
    db.add(tp)
    db.commit()
    db.refresh(tp)
    return tp


def update_tenant_product(
    db: Session, tenant_product_id: str, data: TenantProductUpdate
) -> TenantProduct | None:
    tp = get_tenant_product(db, tenant_product_id)
    if not tp:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(tp, field, value)
    db.commit()
    db.refresh(tp)
    return tp


def delete_tenant_product(db: Session, tenant_product_id: str) -> bool:
    tp = get_tenant_product(db, tenant_product_id)
    if not tp:
        return False
    db.delete(tp)
    db.commit()
    return True


def count_tenant_products(db: Session, tenant_id: str) -> int:
    return (
        db.query(func.count(TenantProduct.id))
        .filter(TenantProduct.tenant_id == tenant_id)
        .scalar() or 0
    )


def count_enabled_tenant_products(db: Session, tenant_id: str) -> int:
    return (
        db.query(func.count(TenantProduct.id))
        .filter(
            TenantProduct.tenant_id == tenant_id,
            TenantProduct.is_enabled == True,  # noqa: E712
        )
        .scalar() or 0
    )

