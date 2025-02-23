from __future__ import annotations

from abc import abstractmethod
from typing import Any

from shared.base import BaseModel
from shared.base import BaseService
from shared.models import ExercisesType


class InteractionInput(BaseModel):
    user_answer: str
    correct_answer: str
    exercies_type: ExercisesType


class InteractionOutput(BaseModel):
    response: str


class InteractionService(BaseService):
    @abstractmethod
    def process(self, inputs: Any) -> Any:
        raise NotImplementedError()
