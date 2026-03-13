from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Brand
# ---------------------------------------------------------------------------

class BrandBase(BaseModel):
    name: str
    website_url: str | None = None


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: str | None = None
    website_url: str | None = None


class BrandRead(BrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# ProductLine
# ---------------------------------------------------------------------------

class ProductLineBase(BaseModel):
    name: str
    category: str


class ProductLineCreate(ProductLineBase):
    brand_id: str


class ProductLineUpdate(BaseModel):
    name: str | None = None
    category: str | None = None


class ProductLineRead(ProductLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    brand_id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class ProductBase(BaseModel):
    sku: str | None = None
    code: str
    name: str
    tone_family: str | None = None
    pack_size_value: float | None = None
    pack_size_unit: str | None = None
    is_active: bool = True


class ProductCreate(ProductBase):
    product_line_id: str


class ProductUpdate(BaseModel):
    sku: str | None = None
    code: str | None = None
    name: str | None = None
    tone_family: str | None = None
    pack_size_value: float | None = None
    pack_size_unit: str | None = None
    is_active: bool | None = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_line_id: str
    created_at: datetime





