import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    default_location_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    # ADMIN | MANAGER | EMPLOYEE
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="EMPLOYEE")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship(  # type: ignore[name-defined]
        "Tenant", back_populates="users"
    )
    default_location: Mapped["Location | None"] = relationship(  # type: ignore[name-defined]
        "Location", back_populates="users", foreign_keys=[default_location_id]
    )
    formulas: Mapped[list["Formula"]] = relationship(  # type: ignore[name-defined]
        "Formula", back_populates="created_by_user"
    )
    inventory_txns: Mapped[list["InventoryTxn"]] = relationship(  # type: ignore[name-defined]
        "InventoryTxn", back_populates="user"
    )


