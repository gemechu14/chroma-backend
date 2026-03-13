from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from src.crud import customer as crud
from src.utils.deps import get_current_user
from src.utils.pagination import PaginatedResponse, calculate_skip, calculate_total_pages
from src.models.user import User

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=PaginatedResponse[CustomerRead])
def list_customers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if search:
        items = crud.search_customers(db, current_user.tenant_id, search, limit=page_size)
        total = crud.count_customers_search(db, current_user.tenant_id, search)
    else:
        skip = calculate_skip(page, page_size)
        items = crud.get_customers_by_tenant(db, current_user.tenant_id, skip=skip, limit=page_size)
        total = crud.count_customers_by_tenant(db, current_user.tenant_id)
    
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data.tenant_id = current_user.tenant_id
    return crud.create_customer(db, data)


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = crud.get_customer(db, customer_id)
    if not customer or customer.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.patch("/{customer_id}", response_model=CustomerRead)
def update_customer(
    customer_id: str,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = crud.get_customer(db, customer_id)
    if not customer or customer.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return crud.update_customer(db, customer_id, data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = crud.get_customer(db, customer_id)
    if not customer or customer.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    crud.delete_customer(db, customer_id)

