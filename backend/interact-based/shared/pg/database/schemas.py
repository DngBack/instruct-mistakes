from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class Identified(BaseModel):
    id: str


class Dated(BaseModel):
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    deletedAt: datetime | None = None


class DatabaseSchema(Identified, Dated):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class UserTracking(DatabaseSchema):
    user_id: str
    exercises_type: str
    user_answer: str
    correct_answer: str
    responses: str
