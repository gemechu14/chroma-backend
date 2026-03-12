"""Pagination utilities for converting page/page_size to skip/limit."""
from typing import TypeVar, Generic

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response schema."""
    items: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int


def calculate_skip(page: int, page_size: int) -> int:
    """Calculate skip value from page and page_size."""
    return (page - 1) * page_size if page > 0 else 0


def calculate_total_pages(total: int, page_size: int) -> int:
    """Calculate total number of pages."""
    return (total + page_size - 1) // page_size if page_size > 0 else 0


def paginate_query(page: int = Field(default=1, ge=1), page_size: int = Field(default=20, ge=1, le=100)):
    """Dependency function for pagination parameters."""
    return {"page": page, "page_size": page_size}


