from __future__ import annotations

from functools import cached_property

from domain.interactive import InteractionInput
from domain.interactive import InteractionOutput
from domain.interactive import LLMInteractionService
from infra.llm_service import OpenAIService
from shared.base import BaseModel
from shared.base import BaseService
from shared.logging import get_logger
from shared.models import ExercisesType
from shared.settings import load_settings
from shared.settings import Settings

logger = get_logger(__name__)


class InteractBasedInput(BaseModel):
    user_answer: str
    correct_answer: str
    exercies_type: ExercisesType


class InteractBasedOutput(BaseModel):
    response: str


class InteractBasedService(BaseService):
    @cached_property
    def settings(self) -> Settings:
        return load_settings()

    @cached_property
    def llm_model(self) -> OpenAIService:
        return OpenAIService(settings=self.settings.openai)

    @cached_property
    def interaction_service(self) -> LLMInteractionService:
        return LLMInteractionService(llm_model=self.llm_model)

    def process(self, inputs: InteractBasedInput) -> InteractBasedOutput:
        response = self._interact_llm(
            inputs=InteractionInput(
                user_answer=inputs.user_answer,
                correct_answer=inputs.correct_answer,
                exercies_type=inputs.exercies_type,
            ),
        ).response
        return InteractBasedOutput(response=response)

    def _interact_llm(self, inputs: InteractionInput) -> InteractionOutput:
        return self.interaction_service.process(inputs=inputs)
