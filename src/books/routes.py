from fastapi import APIRouter, status
from src.books.book_data import books
from src.books.schemas import Book
from typing import List



book_router = APIRouter()

@book_router.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books():
    return books