import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    plan: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # active | trial | suspended
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="trial")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    locations: Mapped[list["Location"]] = relationship(
        "Location", back_populates="tenant", cascade="all, delete-orphan"
    )
    users: Mapped[list["User"]] = relationship(  # type: ignore[name-defined]
        "User", back_populates="tenant", cascade="all, delete-orphan"
    )
    customers: Mapped[list["Customer"]] = relationship(  # type: ignore[name-defined]
        "Customer", back_populates="tenant", cascade="all, delete-orphan"
    )
    tenant_products: Mapped[list["TenantProduct"]] = relationship(  # type: ignore[name-defined]
        "TenantProduct", back_populates="tenant", cascade="all, delete-orphan"
    )


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str | None] = mapped_column(nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="locations")
    users: Mapped[list["User"]] = relationship(  # type: ignore[name-defined]
        "User", back_populates="default_location", foreign_keys="User.default_location_id"
    )
    customers: Mapped[list["Customer"]] = relationship(  # type: ignore[name-defined]
        "Customer", back_populates="home_location", foreign_keys="Customer.home_location_id"
    )
    inventory_items: Mapped[list["InventoryItem"]] = relationship(  # type: ignore[name-defined]
        "InventoryItem", back_populates="location", cascade="all, delete-orphan"
    )
    formulas: Mapped[list["Formula"]] = relationship(  # type: ignore[name-defined]
        "Formula", back_populates="location"
    )

