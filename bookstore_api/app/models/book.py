import datetime

from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins import TransactionMixin

# Use TYPE_CHECKING block to import models ONLY during static analysis
# and not at runtime.
if TYPE_CHECKING:
    from . import Review
    from . import Author

class Book(TransactionMixin):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Foreign key to Author
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'), nullable=False)

    author: Mapped['Author'] = relationship('Author', back_populates='books')
    reviews: Mapped[List['Review']] = relationship('Review', back_populates='book')
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<Book %r>' % self.title
