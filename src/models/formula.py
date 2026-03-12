import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Formula(Base):
    __tablename__ = "formulas"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    location_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("locations.id", ondelete="RESTRICT"), nullable=False
    )
    customer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    created_by_user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    formula_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    service_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    location: Mapped["Location"] = relationship(  # type: ignore[name-defined]
        "Location", back_populates="formulas"
    )
    customer: Mapped["Customer"] = relationship(  # type: ignore[name-defined]
        "Customer", back_populates="formulas"
    )
    created_by_user: Mapped["User"] = relationship(  # type: ignore[name-defined]
        "User", back_populates="formulas"
    )
    formula_items: Mapped[list["FormulaItem"]] = relationship(
        "FormulaItem", back_populates="formula", cascade="all, delete-orphan"
    )
    inventory_txns: Mapped[list["InventoryTxn"]] = relationship(  # type: ignore[name-defined]
        "InventoryTxn", back_populates="formula"
    )


class FormulaItem(Base):
    __tablename__ = "formula_items"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    formula_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("formulas.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tenant_product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tenant_products.id", ondelete="RESTRICT"),
        nullable=False,
    )
    # Amount in grams or milliliters
    amount_used: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    cost_at_time: Mapped[float | None] = mapped_column(Numeric(12, 4), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    formula: Mapped["Formula"] = relationship("Formula", back_populates="formula_items")
    tenant_product: Mapped["TenantProduct"] = relationship(  # type: ignore[name-defined]
        "TenantProduct", back_populates="formula_items"
    )


