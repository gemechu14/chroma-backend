import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class TenantProduct(Base):
    __tablename__ = "tenant_products"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )
    custom_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # G | ML
    tracking_unit: Mapped[str] = mapped_column(String(10), nullable=False, default="G")
    default_unit_cost: Mapped[float | None] = mapped_column(Numeric(12, 4), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    tenant: Mapped["Tenant"] = relationship(  # type: ignore[name-defined]
        "Tenant", back_populates="tenant_products"
    )
    product: Mapped["Product"] = relationship(  # type: ignore[name-defined]
        "Product", back_populates="tenant_products"
    )
    inventory_items: Mapped[list["InventoryItem"]] = relationship(  # type: ignore[name-defined]
        "InventoryItem", back_populates="tenant_product", cascade="all, delete-orphan"
    )
    formula_items: Mapped[list["FormulaItem"]] = relationship(  # type: ignore[name-defined]
        "FormulaItem", back_populates="tenant_product"
    )





