import datetime

from typing import TYPE_CHECKING
from sqlalchemy import (
    Integer, DateTime, Text, CheckConstraint, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins import TransactionMixin


# Use TYPE_CHECKING block to import models ONLY during static analysis
# and not at runtime.
if TYPE_CHECKING:
    from . import User, Book

class Review(TransactionMixin):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Foreign key to User & Book
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='reviews')
    book: Mapped['Book'] = relationship('Book', back_populates='reviews')

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # Adds a table-level CheckConstraint for ratings from 1 to 5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='ck_rating_range'),
        UniqueConstraint('book_id', 'user_id', name='_user_book_review_uc'),
    )

    def __repr__(self):
        return f'<Review {self.rating}>'
