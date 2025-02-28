from __future__ import annotations

from shared.base import BaseModel


class PostgresDB(BaseModel):
    username: str
    password: str
    db: str
    host: str
