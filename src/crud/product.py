from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.product import Brand, ProductLine, Product
from src.schemas.product import (
    BrandCreate,
    BrandUpdate,
    ProductLineCreate,
    ProductLineUpdate,
    ProductCreate,
    ProductUpdate,
)


# ---------------------------------------------------------------------------
# Brand
# ---------------------------------------------------------------------------

def get_brand(db: Session, brand_id: str) -> Brand | None:
    return db.query(Brand).filter(Brand.id == brand_id).first()


def get_brands(db: Session, skip: int = 0, limit: int = 100) -> list[Brand]:
    return db.query(Brand).offset(skip).limit(limit).all()


def create_brand(db: Session, data: BrandCreate) -> Brand:
    brand = Brand(**data.model_dump())
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


def update_brand(db: Session, brand_id: str, data: BrandUpdate) -> Brand | None:
    brand = get_brand(db, brand_id)
    if not brand:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(brand, field, value)
    db.commit()
    db.refresh(brand)
    return brand


def delete_brand(db: Session, brand_id: str) -> bool:
    brand = get_brand(db, brand_id)
    if not brand:
        return False
    db.delete(brand)
    db.commit()
    return True


# ---------------------------------------------------------------------------
# ProductLine
# ---------------------------------------------------------------------------

def get_product_line(db: Session, product_line_id: str) -> ProductLine | None:
    return db.query(ProductLine).filter(ProductLine.id == product_line_id).first()


def get_product_lines_by_brand(
    db: Session, brand_id: str, skip: int = 0, limit: int = 100
) -> list[ProductLine]:
    return (
        db.query(ProductLine)
        .filter(ProductLine.brand_id == brand_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_product_line(db: Session, data: ProductLineCreate) -> ProductLine:
    product_line = ProductLine(**data.model_dump())
    db.add(product_line)
    db.commit()
    db.refresh(product_line)
    return product_line


def update_product_line(
    db: Session, product_line_id: str, data: ProductLineUpdate
) -> ProductLine | None:
    product_line = get_product_line(db, product_line_id)
    if not product_line:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(product_line, field, value)
    db.commit()
    db.refresh(product_line)
    return product_line


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

def get_product(db: Session, product_id: str) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_products_by_line(
    db: Session, product_line_id: str, skip: int = 0, limit: int = 200
) -> list[Product]:
    return (
        db.query(Product)
        .filter(Product.product_line_id == product_line_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_products(db: Session, skip: int = 0, limit: int = 200) -> list[Product]:
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: str, data: ProductUpdate) -> Product | None:
    product = get_product(db, product_id)
    if not product:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def count_brands(db: Session) -> int:
    return db.query(func.count(Brand.id)).scalar() or 0


def count_product_lines_by_brand(db: Session, brand_id: str) -> int:
    return (
        db.query(func.count(ProductLine.id))
        .filter(ProductLine.brand_id == brand_id)
        .scalar() or 0
    )


def count_products_by_line(db: Session, product_line_id: str) -> int:
    return (
        db.query(func.count(Product.id))
        .filter(Product.product_line_id == product_line_id)
        .scalar() or 0
    )


def count_products(db: Session) -> int:
    return db.query(func.count(Product.id)).scalar() or 0

