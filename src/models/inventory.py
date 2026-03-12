import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    __table_args__ = (
        UniqueConstraint("location_id", "tenant_product_id", name="uq_inventory_location_product"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    location_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tenant_product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant_products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Stored in grams or milliliters per tracking_unit
    on_hand_qty: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    reorder_level_qty: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    location: Mapped["Location"] = relationship(  # type: ignore[name-defined]
        "Location", back_populates="inventory_items"
    )
    tenant_product: Mapped["TenantProduct"] = relationship(  # type: ignore[name-defined]
        "TenantProduct", back_populates="inventory_items"
    )
    transactions: Mapped[list["InventoryTxn"]] = relationship(
        "InventoryTxn", back_populates="inventory_item", cascade="all, delete-orphan"
    )


class InventoryTxn(Base):
    __tablename__ = "inventory_txns"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    inventory_item_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("inventory_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    formula_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("formulas.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    # PURCHASE | CONSUME | ADJUST | WASTE | RETURN
    txn_type: Mapped[str] = mapped_column(String(20), nullable=False)
    # Positive = stock in, negative = stock out
    qty_delta: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    unit_cost_at_time: Mapped[float | None] = mapped_column(Numeric(12, 4), nullable=True)
    note: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    inventory_item: Mapped["InventoryItem"] = relationship(
        "InventoryItem", back_populates="transactions"
    )
    formula: Mapped["Formula | None"] = relationship(  # type: ignore[name-defined]
        "Formula", back_populates="inventory_txns"
    )
    user: Mapped["User"] = relationship(  # type: ignore[name-defined]
        "User", back_populates="inventory_txns"
    )


