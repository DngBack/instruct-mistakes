from __future__ import annotations

from typing import Union

from openai import OpenAI
from shared.base import BaseModel
from shared.logging import get_logger
from shared.settings import OpenAISettings

from ..base.llm_base_service import LLMBaseService

logger = get_logger(__name__)


class OpenAIInput(BaseModel):
    user_prompt: str
    system_prompt: str = ''
    json_mode: bool = False


class OpenAIOutput(BaseModel):
    response: Union[str, dict]


class OpenAIService(LLMBaseService):
    settings: OpenAISettings

    @property
    def client(self) -> OpenAI:
        """
        Create a OpenAIService client

        Returns:
            OpenAIClient: OpenAI service client
        """
        try:
            return OpenAI(api_key=self.settings.openai_api_key)
        except Exception as e:
            logger.exception(
                f'Error occurred while creating OpenAI client: {str(e)}',
                extra={},
            )
            raise e

    def process(self, inputs: OpenAIInput) -> OpenAIOutput:
        """
        Process user input using OpenAI

        Args:
            system_prompt (str): System prompt
            user_prompt (str): User prompt
            json_mode (bool): Whether to parse response as JSON

        Returns:
            OpenAIOutput: OpenAI response
        """
        try:
            response = self._inference_by_llm(
                inputs.system_prompt,
                inputs.user_prompt,
                inputs.json_mode,
            )
            return OpenAIOutput(response=response)
        except Exception as e:
            logger.exception(
                f'Error occurred while processing OpenAI input: {str(e)}',
                extra={},
            )
            raise e

    def _inference_by_llm(
        self,
        system_prompt: str,
        user_prompt: str,
        json_mode: bool,
    ) -> str:
        if system_prompt:
            messages = self._get_system_users_messages(
                user_prompt, system_prompt,
            )
        else:
            messages = self._get_users_messages(user_prompt)

        response = self.client.chat.completions.create(
            model=self.settings.openai_model,
            stream=self.settings.openai_stream,
            max_tokens=self.settings.max_tokens,
            temperature=self.settings.temperature,
            top_p=self.settings.top_p,
            messages=messages,
        )
        response = response.choices[0].message.content
        if json_mode:
            return self.json_parse(response)
        return response

    def _get_users_messages(self, user_prompt: str) -> list[dict]:
        return [{'role': 'user', 'content': user_prompt}]

    def _get_system_users_messages(
        self,
        user_prompt: str,
        system_prompt: str,
    ) -> list[dict]:
        return [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ]
