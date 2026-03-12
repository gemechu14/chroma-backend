from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.formula import FormulaCreate, FormulaRead, FormulaUpdate
from src.crud import formula as crud
from src.crud.formula import InsufficientInventoryError
from src.utils.deps import get_current_user, require_role
from src.utils.pagination import PaginatedResponse, calculate_skip, calculate_total_pages
from src.models.user import User

router = APIRouter(prefix="/formulas", tags=["Formulas"])


@router.get("/", response_model=PaginatedResponse[FormulaRead])
def list_formulas(
    customer_id: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skip = calculate_skip(page, page_size)
    if customer_id:
        items = crud.get_formulas_by_customer(
            db, current_user.tenant_id, customer_id, skip=skip, limit=page_size
        )
        total = crud.count_formulas_by_customer(db, current_user.tenant_id, customer_id)
    else:
        items = crud.get_formulas_by_tenant(db, current_user.tenant_id, skip=skip, limit=page_size)
        total = crud.count_formulas_by_tenant(db, current_user.tenant_id)
    
    return PaginatedResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=calculate_total_pages(total, page_size),
    )


@router.post("/", response_model=FormulaRead, status_code=status.HTTP_201_CREATED)
def create_formula(
    data: FormulaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a formula and automatically deduct inventory for each product used.
    The `created_by_user_id` is set from the authenticated user.
    
    Validates inventory sufficiency before creating the formula.
    Returns 400 Bad Request if inventory is insufficient.
    """
    data.tenant_id = current_user.tenant_id
    data.created_by_user_id = current_user.id
    try:
        return crud.create_formula(db, data)
    except InsufficientInventoryError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Insufficient inventory",
                "message": "One or more products do not have sufficient inventory",
                "insufficient_items": e.insufficient_items
            }
        )


@router.get("/{formula_id}", response_model=FormulaRead)
def get_formula(
    formula_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    formula = crud.get_formula(db, formula_id)
    if not formula or formula.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formula not found")
    return formula


@router.patch("/{formula_id}", response_model=FormulaRead)
def update_formula(
    formula_id: str,
    data: FormulaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    formula = crud.get_formula(db, formula_id)
    if not formula or formula.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formula not found")
    return crud.update_formula(db, formula_id, data)


@router.delete("/{formula_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_formula(
    formula_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN", "MANAGER")),
):
    formula = crud.get_formula(db, formula_id)
    if not formula or formula.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formula not found")
    crud.delete_formula(db, formula_id)

