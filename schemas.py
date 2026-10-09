from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class CategoryResponse(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    isbn: str = Field(..., min_length=1)
    publication_year: Optional[int] = Field(None, ge=0)
    stock_quantity: int = Field(1, ge=0)
    category_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    isbn: Optional[str] = Field(None, min_length=1)
    publication_year: Optional[int] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class BookResponse(BookCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
