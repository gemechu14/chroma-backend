from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.tenant import Tenant, Location
from src.schemas.tenant import TenantCreate, TenantUpdate, LocationCreate, LocationUpdate


# ---------------------------------------------------------------------------
# Tenant CRUD
# ---------------------------------------------------------------------------

def get_tenant(db: Session, tenant_id: str) -> Tenant | None:
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()


def get_tenants(db: Session, skip: int = 0, limit: int = 100) -> list[Tenant]:
    return db.query(Tenant).offset(skip).limit(limit).all()


def create_tenant(db: Session, data: TenantCreate) -> Tenant:
    tenant = Tenant(**data.model_dump())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


def update_tenant(db: Session, tenant_id: str, data: TenantUpdate) -> Tenant | None:
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(tenant, field, value)
    db.commit()
    db.refresh(tenant)
    return tenant


def delete_tenant(db: Session, tenant_id: str) -> bool:
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        return False
    db.delete(tenant)
    db.commit()
    return True


# ---------------------------------------------------------------------------
# Location CRUD
# ---------------------------------------------------------------------------

def get_location(db: Session, location_id: str) -> Location | None:
    return db.query(Location).filter(Location.id == location_id).first()


def get_locations_by_tenant(
    db: Session, tenant_id: str, skip: int = 0, limit: int = 100
) -> list[Location]:
    return (
        db.query(Location)
        .filter(Location.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_location(db: Session, data: LocationCreate) -> Location:
    location = Location(**data.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(db: Session, location_id: str, data: LocationUpdate) -> Location | None:
    location = get_location(db, location_id)
    if not location:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    return location


def delete_location(db: Session, location_id: str) -> bool:
    location = get_location(db, location_id)
    if not location:
        return False
    db.delete(location)
    db.commit()
    return True


def count_tenants(db: Session) -> int:
    return db.query(func.count(Tenant.id)).scalar() or 0


def count_locations_by_tenant(db: Session, tenant_id: str) -> int:
    return (
        db.query(func.count(Location.id))
        .filter(Location.tenant_id == tenant_id)
        .scalar() or 0
    )

