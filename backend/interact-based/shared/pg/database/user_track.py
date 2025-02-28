from __future__ import annotations

from collections.abc import Sequence
from functools import partial
from typing import cast

from shared.logging import get_logger
from sqlalchemy.orm import Session

from ..models import UserTracking as UserTrackingModel
from .schemas import UserTracking
from .utils import _delete
from .utils import _get_data
from .utils import _get_data_by_id
from .utils import _insert
from .utils import _update

logger = get_logger(__name__)


_insert_method = partial(_insert, logger, UserTrackingModel, UserTracking)
_update_method = partial(_update, logger, UserTrackingModel, UserTracking)
_delete_method = partial(_delete, logger, UserTrackingModel, UserTracking)
_get_method = partial(_get_data, logger, UserTrackingModel, UserTracking)
_get_by_id_method = partial(
    _get_data_by_id, logger,
    UserTrackingModel, UserTracking,
)


class UserController:
    def insert_UserTracking(self, session: Session, model: UserTracking) -> UserTracking:
        """Insert UserTracking to database

        Args:
            session (Session): Database Session
            UserTracking (UserTracking): UserTracking data

        Returns:
            UserTracking: return inserted UserTracking
        """
        return cast(UserTracking, _insert_method(session, model))

    def update_UserTracking(self, session: Session, model: UserTracking) -> UserTracking | None:
        """Update UserTracking in database

        Args:
            session (Session): Database Session
            UserTracking (UserTracking): UserTracking data

        Returns:
            UserTracking | None: return updated UserTracking or None if no update
        """
        result = _update_method(session, model)
        return cast(UserTracking, result) if result else None

    def delete_UserTracking(self, session: Session, id: str) -> UserTracking | None:
        """Delete UserTracking in database

        Args:
            session (Session): Database Session
            UserTracking (UserTracking): UserTracking data

        Returns:
            UserTracking | None: return deleted UserTracking or None if no update
        """
        result = _delete_method(session, id)
        return cast(UserTracking, result) if result else None

    def get_UserTrackings(
        self,
        session: Session,
        filter: dict[str, object] | None = None,
        order_by: Sequence | None = None,
        limit: int | None = None,
    ) -> list[UserTracking] | None:
        """Get UserTrackings with applied filter and limit (if None not applied)

        Args:
            session (Session): Database Session
            filter (dict[str, object] | None, optional): filter kwargs, if None will apply no filter. Defaults to None.
            limit (int | None, optional): Limit results returned, if None will return all results. Defaults to None.


        Returns:
            list[UserTracking] | None: UserTrackings fetched, None if not found
        """
        result = _get_method(session, filter, order_by, limit)
        return cast(list[UserTracking], result) if result else None

    def get_UserTracking_by_id(self, session: Session, id: str) -> UserTracking | None:
        """Get UserTracking with provided id

        Args:
            session (Session): Database Session
            id (int): UserTracking id to fetch


        Returns:
            UserTracking | None: UserTracking fetched or None if not found
        """
        result = _get_by_id_method(session, id)
        return cast(UserTracking, result) if result else None
