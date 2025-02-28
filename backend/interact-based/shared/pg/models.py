from __future__ import annotations

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Dated(Base):
    __abstract__ = True

    createdAt: Mapped[datetime] = mapped_column(insert_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(
        onupdate=func.now(), nullable=True,
    )
    deletedAt: Mapped[datetime] = mapped_column(nullable=True)


class Identified(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(primary_key=True, index=True)


class UserTracking(Identified, Dated):
    __tablename__ = 'user_tracking'

    user_id: Mapped[str]
    exercises_type: Mapped[str]
    user_answer: Mapped[str]
    correct_answer: Mapped[str]
    responses: Mapped[str]
