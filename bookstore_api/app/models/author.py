import datetime

from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bookstore_api.app.extensions import Base

# Use TYPE_CHECKING block to import models ONLY during static analysis
# and not at runtime.
if TYPE_CHECKING:
    from .book import Book

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    books: Mapped[List['Book']] = relationship('Book', back_populates='author')
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=False)

    def __repr__(self):
        return '<Author %r>' % self.name
