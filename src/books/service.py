from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from .models import Book
from sqlmodel import select, desc
from datetime import datetime
import uuid

class BookService:
    # get all books
    async def get_all_book(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    # get book by uid
    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    # create book
    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.published_date = datetime.strftime(book_data.published_date, "%Y-%m-%d")
        if isinstance(new_book.published_date, str):
            new_book.published_date = datetime.strptime(
                new_book.published_date, "%Y-%m-%d"
            ).date()
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
    
    # update book
    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_data_dict.items():
                setattr(book_to_update, key, value)
            await session.commit()
            await session.refresh(book_to_update)
            return book_to_update 
        else:
            return None
        
    # delete book
    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete:
            try:
                await session.delete(book_to_delete)
                await session.commit()
                return True
            except Exception:
                await session.rollback()
                raise 
            
        return None

    
