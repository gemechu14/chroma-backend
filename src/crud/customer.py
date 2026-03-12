from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.customer import Customer
from src.schemas.customer import CustomerCreate, CustomerUpdate


def get_customer(db: Session, customer_id: str) -> Customer | None:
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customers_by_tenant(
    db: Session, tenant_id: str, skip: int = 0, limit: int = 100
) -> list[Customer]:
    return (
        db.query(Customer)
        .filter(Customer.tenant_id == tenant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def search_customers(
    db: Session, tenant_id: str, query: str, limit: int = 20
) -> list[Customer]:
    pattern = f"%{query}%"
    return (
        db.query(Customer)
        .filter(
            Customer.tenant_id == tenant_id,
            (Customer.full_name.ilike(pattern) | Customer.phone.ilike(pattern)),
        )
        .limit(limit)
        .all()
    )


def create_customer(db: Session, data: CustomerCreate) -> Customer:
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer_id: str, data: CustomerUpdate) -> Customer | None:
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: str) -> bool:
    customer = get_customer(db, customer_id)
    if not customer:
        return False
    db.delete(customer)
    db.commit()
    return True


def count_customers_by_tenant(db: Session, tenant_id: str) -> int:
    return (
        db.query(func.count(Customer.id))
        .filter(Customer.tenant_id == tenant_id)
        .scalar() or 0
    )


def count_customers_search(db: Session, tenant_id: str, query: str) -> int:
    pattern = f"%{query}%"
    return (
        db.query(func.count(Customer.id))
        .filter(
            Customer.tenant_id == tenant_id,
            (Customer.full_name.ilike(pattern) | Customer.phone.ilike(pattern)),
        )
        .scalar() or 0
    )

