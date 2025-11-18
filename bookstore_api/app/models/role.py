import datetime

from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins import TransactionMixin

# Use TYPE_CHECKING block to import models ONLY during static analysis
# and not at runtime.
if TYPE_CHECKING:
    from . import User

class Role(TransactionMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[List['User']] = relationship('User', back_populates='role')

    def __repr__(self):
        return '<Role %r>' % self.name
