import datetime

from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bookstore_api.app.extensions import Base

# Use TYPE_CHECKING block to import models ONLY during static analysis
# and not at runtime.
if TYPE_CHECKING:
    from .review import Review

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    reviews: Mapped[List['Review']] = relationship('Review', back_populates='user')
    
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
