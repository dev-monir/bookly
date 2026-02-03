from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.books.schemas import Book, BookCreateModel, BookUpdateModel
from src.db.main import get_session
from typing import List
import uuid


book_router = APIRouter()
book_service = BookService()

# book list endpoint
@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_book(session: AsyncSession=Depends(get_session)):
    books = await book_service.get_all_book(session)
    return books

# get book by uid endpoint
@book_router.get("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_uid(book_uid: str, session: AsyncSession=Depends(get_session))->dict:
    book = await book_service.get_book(book_uid, session)
    if book is not None:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# create book endpoint
@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel, session: AsyncSession=Depends(get_session)):
    new_book = await book_service.create_book(book_data, session)
    return new_book

# update book endpoint
@book_router.patch("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession=Depends(get_session))->dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
# delete book endpoint
@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
        )
    
    return None
