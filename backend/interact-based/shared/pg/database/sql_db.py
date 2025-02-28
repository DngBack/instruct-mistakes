from __future__ import annotations

from contextlib import contextmanager
from functools import cached_property

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from ..models import Base
from .user_track import UserController


class SQLDatabase(UserController):
    @cached_property
    def sessionmaker(self) -> sessionmaker:
        engine = create_engine(
            f'postgresql+psycopg2://{self.username}:{self.password}@{self.host}/{self.db}',
        )
        Base.metadata.create_all(engine)
        return sessionmaker(autoflush=False, bind=engine)

    def __init__(self, username, password, host, db):
        self.username = username
        self.password = password
        self.host = host
        self.db = db

    @contextmanager
    def get_session(self):
        try:
            session: Session = self.sessionmaker()
            yield session
        finally:
            session.close()  # type: ignore
