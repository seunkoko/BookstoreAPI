import datetime

from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bookstore_api.app.extensions import Base

# Use TYPE_CHECKING block to import models ONLY during static analysis
# and not at runtime.
if TYPE_CHECKING:
    from .review import Review
    from .author import Author

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Foreign key to Author
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'), nullable=False)

    author: Mapped['Author'] = relationship('Author', back_populates='books')
    reviews: Mapped[List['Review']] = relationship('Review', back_populates='book')
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title
