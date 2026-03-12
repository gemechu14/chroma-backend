from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.utils.security import hash_password


def get_user(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str, tenant_id: str) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email, User.tenant_id == tenant_id)
        .first()
    )


def get_users_by_email(db: Session, email: str) -> list[User]:
    """Get all users with the given email (across all tenants)."""
    return db.query(User).filter(User.email == email).all()


def get_users_by_tenant(
    db: Session, tenant_id: str, skip: int = 0, limit: int = 100
) -> list[User]:
    return (
        db.query(User)
        .filter(User.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user(db: Session, data: UserCreate) -> User:
    payload = data.model_dump(exclude={"password"})
    payload["password_hash"] = hash_password(data.password)
    user = User(**payload)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: str, data: UserUpdate) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None
    update_data = data.model_dump(exclude_none=True)
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def count_users_by_tenant(db: Session, tenant_id: str) -> int:
    return (
        db.query(func.count(User.id))
        .filter(User.tenant_id == tenant_id)
        .scalar() or 0
    )

