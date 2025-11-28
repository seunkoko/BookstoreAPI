import datetime

from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins import TransactionMixin

# Use TYPE_CHECKING block to import models ONLY during static analysis
# and not at runtime.
if TYPE_CHECKING:
    from . import Book

class BookCategory(TransactionMixin):
    __tablename__ = "book_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    books: Mapped[List['Book']] = relationship('Book', back_populates='category')

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return f'<BookCategory {self.name}>'
