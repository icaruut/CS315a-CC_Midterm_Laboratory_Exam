from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud, models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Inventory API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Categories ----------------
@app.post("/categories/", response_model=schemas.CategoryResponse,
          status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    if crud.get_category_by_name(db, category.name):
        raise HTTPException(status_code=400, detail="Category name already exists")
    return crud.create_category(db, category)


@app.get("/categories/", response_model=List[schemas.CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


# ---------------- Books ----------------
@app.post("/books/", response_model=schemas.BookResponse,
          status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if not crud.get_category(db, book.category_id):
        raise HTTPException(status_code=400, detail="Category does not exist")
    if crud.get_book_by_isbn(db, book.isbn):
        raise HTTPException(status_code=400, detail="ISBN already exists")
    return crud.create_book(db, book)


@app.get("/books/", response_model=List[schemas.BookResponse])
def list_books(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_books(db, category_id)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, data: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if data.category_id is not None and not crud.get_category(db, data.category_id):
        raise HTTPException(status_code=400, detail="Category does not exist")
    if data.isbn is not None and data.isbn != book.isbn and crud.get_book_by_isbn(db, data.isbn):
        raise HTTPException(status_code=400, detail="ISBN already exists")
    return crud.update_book(db, book, data)


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, book)
    return {"detail": "Book deleted"}
