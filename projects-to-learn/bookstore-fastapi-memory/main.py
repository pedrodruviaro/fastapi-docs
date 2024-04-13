from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from random import randint, choice
from datetime import date

app = FastAPI()


def generate_id() -> str:
    return str(randint(1, 100000))


class Genre(str, Enum):
    fiction = "fiction"
    non_fiction = "non-fiction"
    fantasy = "fantasy"
    mistery = "mistery"


class Book(BaseModel):
    id: Optional[str] = Field(default_factory=generate_id, alias="_id")
    title: str
    author: str
    genre: Genre
    publish_date: date


books: list[Book] = [Book(title=f"{i} Harry Potter", author=f"Pedro {
                          i} Ruviaro", genre=choice(list(Genre)), publish_date=date(2024, 1, i + 1)) for i in range(5)]


def get_book_by_id(id: str) -> Optional[Book]:
    for book in books:
        if book.id == id:
            return book
    return None


@app.get('/')
async def root():
    """
    Root endpoint to check if the API is available
    """
    return {"message": "All set!"}


@app.get('/books')
async def get_books():
    """
    Get all books in database
    """
    return {"count": len(books), "data": books}


@app.get("/books/{id}")
async def get_book(id: str):
    """
    Get a single book by id
    """
    book = get_book_by_id(id)
    if book:
        return {"data": book}

    raise HTTPException(status_code=404, detail=f"Book with id {id} not found")


@app.post('/books')
async def create_book(book: Book):
    """
    Create a book 
    """
    id = generate_id()
    book.id = id
    books.append(book)
    return {"count": len(books), "data": books}


@app.put("/books/{id}")
async def update_book(id: str, updated_book: Book):
    """
    Update a book by id
    """
    for idx, book in enumerate(books):
        if book.id == id:
            updated_book.id = id
            books[idx] = updated_book
            return {"data": books[idx]}

    raise HTTPException(status_code=404, detail=f"Book with id {id} not found")


@app.delete("/books/{id}")
async def delete_book(id: str):
    """
    Delete a book by id
    """
    for idx, book in enumerate(books):
        if book.id == id:
            del books[idx]
            return {"count": len(books), "data": books}

    raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
