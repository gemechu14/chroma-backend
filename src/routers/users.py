from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.user import UserCreate, UserRead, UserUpdate, Token, TokenRefresh, LoginRequest
from src.crud import user as crud
from src.utils.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token
from src.utils.deps import get_current_user, require_role
from src.utils.pagination import PaginatedResponse, calculate_skip, calculate_total_pages
from src.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user with email and password only.
    Searches for users by email and validates password.
    """
    users = crud.get_users_by_email(db, email=login_data.email)
    
    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check password against all matching users
    valid_user = None
    for user in users:
        if verify_password(login_data.password, user.password_hash) and user.is_active:
            valid_user = user
            break
    
    if not valid_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login timestamp
    valid_user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    token_data = {"sub": valid_user.id, "tenant_id": valid_user.tenant_id}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
def refresh_token(
    data: TokenRefresh,
    db: Session = Depends(get_db),
):
    """Refresh an access token using a valid refresh token."""
    payload = decode_refresh_token(data.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    if not user_id or not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    user = crud.get_user(db, user_id)
    if not user or not user.is_active or user.tenant_id != tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    token_data = {"sub": user.id, "tenant_id": user.tenant_id}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=PaginatedResponse[UserRead])
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    skip = calculate_skip(page, page_size)
    items = crud.get_users_by_tenant(db, current_user.tenant_id, skip=skip, limit=page_size)
    total = crud.count_users_by_tenant(db, current_user.tenant_id)
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    if current_user.tenant_id != data.tenant_id and current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    existing = crud.get_user_by_email(db, email=data.email, tenant_id=data.tenant_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered for this tenant",
        )
    return crud.create_user(db, data)


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = crud.get_user(db, user_id)
    if not user or user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    user = crud.get_user(db, user_id)
    if not user or user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.update_user(db, user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN")),
):
    user = crud.get_user(db, user_id)
    if not user or user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud.delete_user(db, user_id)

