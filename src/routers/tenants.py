from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.tenant import (
    TenantCreate,
    TenantRead,
    TenantUpdate,
    LocationCreate,
    LocationRead,
    LocationUpdate,
    TenantRegistration,
    TenantRegistrationResponse,
)
from src.schemas.user import UserCreate
from src.crud import tenant as crud
from src.crud import user as user_crud
from src.utils.deps import get_current_user, require_role
from src.utils.pagination import PaginatedResponse, calculate_skip, calculate_total_pages
from src.models.user import User

router = APIRouter(prefix="/tenants", tags=["Tenants"])


# ---------------------------------------------------------------------------
# Tenants
# ---------------------------------------------------------------------------

@router.get("/", response_model=PaginatedResponse[TenantRead])
def list_tenants(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    skip = calculate_skip(page, page_size)
    items = crud.get_tenants(db, skip=skip, limit=page_size)
    total = crud.count_tenants(db)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post(
    "/register",
    response_model=TenantRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new tenant",
    description="Public endpoint to register a new tenant, create default location, and admin user.",
)
def register_tenant(
    data: TenantRegistration,
    db: Session = Depends(get_db),
):
    """
    Register a new tenant (salon business).
    
    This endpoint:
    1. Creates a new tenant
    2. Creates a default location
    3. Creates the first admin user
    4. Returns tenant, location, and admin user info
    
    After registration, use the admin email and password to login.
    """
    # Check if email already exists
    existing_users = user_crud.get_users_by_email(db, data.admin_email)
    if existing_users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered. Please use a different email.",
        )
    
    # Create tenant
    tenant_data = TenantCreate(
        name=data.tenant_name,
        plan=data.plan or "trial",
        status="trial",
    )
    tenant = crud.create_tenant(db, tenant_data)
    
    # Create default location
    location_data = LocationCreate(
        tenant_id=tenant.id,
        name=data.location_name,
        address=data.location_address,
        timezone=data.location_timezone,
    )
    location = crud.create_location(db, location_data)
    
    # Create admin user
    admin_user_data = UserCreate(
        tenant_id=tenant.id,
        email=data.admin_email,
        password=data.admin_password,
        full_name=data.admin_full_name,
        role="ADMIN",
        is_active=True,
        default_location_id=location.id,
    )
    admin_user = user_crud.create_user(db, admin_user_data)
    
    return TenantRegistrationResponse(
        tenant=tenant,
        location=location,
        admin_user_id=admin_user.id,
        admin_email=admin_user.email,
        message="Tenant registered successfully. You can now login with your admin credentials.",
    )


@router.post("/", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
def create_tenant(
    data: TenantCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    """Create a tenant (admin only). Use /register for public registration."""
    return crud.create_tenant(db, data)


@router.get("/{tenant_id}", response_model=TenantRead)
def get_tenant(
    tenant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.tenant_id != tenant_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    tenant = crud.get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant


@router.patch("/{tenant_id}", response_model=TenantRead)
def update_tenant(
    tenant_id: str,
    data: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN")),
):
    tenant = crud.update_tenant(db, tenant_id, data)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(
    tenant_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    if not crud.delete_tenant(db, tenant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")


# ---------------------------------------------------------------------------
# Locations (nested under tenant)
# ---------------------------------------------------------------------------

@router.get("/{tenant_id}/locations", response_model=PaginatedResponse[LocationRead])
def list_locations(
    tenant_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.tenant_id != tenant_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    skip = calculate_skip(page, page_size)
    items = crud.get_locations_by_tenant(db, tenant_id, skip=skip, limit=page_size)
    total = crud.count_locations_by_tenant(db, tenant_id)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post(
    "/{tenant_id}/locations",
    response_model=LocationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_location(
    tenant_id: str,
    data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    if current_user.tenant_id != tenant_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    data.tenant_id = tenant_id
    return crud.create_location(db, data)


@router.patch("/{tenant_id}/locations/{location_id}", response_model=LocationRead)
def update_location(
    tenant_id: str,
    location_id: str,
    data: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    if current_user.tenant_id != tenant_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    location = crud.update_location(db, location_id, data)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location


@router.delete(
    "/{tenant_id}/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_location(
    tenant_id: str,
    location_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("ADMIN")),
):
    if not crud.delete_location(db, location_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

