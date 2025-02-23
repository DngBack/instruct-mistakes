from __future__ import annotations

from infra.llm_service import OpenAIInput
from infra.llm_service import OpenAIService
from shared.logging import get_logger
from shared.models import ExercisesType

from .base import InteractionInput
from .base import InteractionOutput
from .base import InteractionService
from .prompt import INTERACTION_SYSTEM_PROMPT
from .prompt import INTERACTION_USERS_PROMPT

logger = get_logger(__name__)


class LLMInteractionService(InteractionService):
    llm_model: OpenAIService

    def process(self, inputs: InteractionInput) -> InteractionOutput:
        user_prompt = self._get_user_inputs(
            user_answer=inputs.user_answer,
            correct_answer=inputs.correct_answer,
            exercies_type=inputs.exercies_type,
        )
        system_prompt = INTERACTION_SYSTEM_PROMPT
        reponse = self._generate_response(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
        )
        return InteractionOutput(response=reponse)

    def _get_user_inputs(
        self,
        user_answer: str,
        correct_answer: str,
        exercies_type: ExercisesType,
    ) -> str:
        user_prompt = INTERACTION_USERS_PROMPT.replace(
            '{exercise_type}',
            str(exercies_type.value),
        )
        user_prompt = user_prompt.replace('{user_answer}', user_answer)
        user_prompt = user_prompt.replace('{correct_answer}', correct_answer)
        return user_prompt

    def _generate_response(self, user_prompt: str, system_prompt: str) -> str:
        response = self.llm_model.process(
            OpenAIInput(user_prompt=user_prompt, system_prompt=system_prompt),
        )
        return response.response
