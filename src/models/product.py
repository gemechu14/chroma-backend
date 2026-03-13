import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    website_url: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product_lines: Mapped[list["ProductLine"]] = relationship(
        "ProductLine", back_populates="brand", cascade="all, delete-orphan"
    )


class ProductLine(Base):
    __tablename__ = "product_lines"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    brand_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("brands.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    # COLOR | DEVELOPER | TONER | TREATMENT
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    brand: Mapped["Brand"] = relationship("Brand", back_populates="product_lines")
    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="product_line", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    product_line_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("product_lines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sku: Mapped[str | None] = mapped_column(String(80), nullable=True)
    # e.g. 09N
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    # e.g. N, G, V
    tone_family: Mapped[str | None] = mapped_column(String(50), nullable=True)
    pack_size_value: Mapped[float | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    # G | ML
    pack_size_unit: Mapped[str | None] = mapped_column(String(10), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product_line: Mapped["ProductLine"] = relationship(
        "ProductLine", back_populates="products"
    )
    tenant_products: Mapped[list["TenantProduct"]] = relationship(  # type: ignore[name-defined]
        "TenantProduct", back_populates="product"
    )





