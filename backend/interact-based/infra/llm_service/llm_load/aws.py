from __future__ import annotations

from typing import Optional
from typing import Union

import boto3
from shared.base import BaseModel
from shared.logging import get_logger
from shared.settings import AWSBedrockSettings

from ..base.llm_base_service import LLMBaseService

logger = get_logger(__name__)


class AWSSonnetInput(BaseModel):
    user_prompt: str
    system_prompt: str = ''
    json_mode: bool = False


class AWSSonnetOutput(BaseModel):
    response: Union[str, dict]


class AWSSonnetService(LLMBaseService):
    settings: AWSBedrockSettings

    @property
    def client(self) -> boto3.client:
        """Create AWSSonnet BedrockRuntime client

        Returns:
            boto3.client: AWSSonnet BedrockRuntime client
        """
        try:
            return boto3.client(
                service_name=self.settings.service_name,
                region_name=self.settings.region,
                aws_access_key_id=self.settings.access_key,
                aws_secret_access_key=self.settings.secret_access_key,
            )
        except Exception as e:
            logger.exception(
                f'Error occurred while creating \
                    AWS Sonnet client: {str(e)}',
                extra={},
            )
            raise e

    def _inference_by_llm(
        self,
        user_prompt: str,
        system_prompt: str,
        json_mode: bool,
    ) -> Optional[Union[str, dict]]:
        """Inference by LLM model

        Args:
            message (list): message list
            system (list): system list
            json_mode (bool): True for JSON mode, False for text mode

        Returns:
            Optional[Union[str, dict]]: response text
        """
        inference_config = {
            'maxTokens': self.settings.max_tokens,
            'temperature': self.settings.temperature,
            'topP': self.settings.top_p,
        }
        message = self._create_user_message(user_prompt)
        if system_prompt:
            system = self._create_system_message(system_prompt)
            response = self.client.converse(
                modelId=self.settings.model_id,
                messages=message,
                system=system,
                inferenceConfig=inference_config,
            )
        else:
            response = self.client.converse(
                modelId=self.settings.model_id,
                messages=message,
                inferenceConfig=inference_config,
            )
        response_text = response['output']['message']['content'][0]['text']

        # parse response to JSON if json_mode is True
        if json_mode:
            return self.json_parse(response_text)
        return response_text

    def process(self, inputs: AWSSonnetInput) -> AWSSonnetOutput:
        """Call request to AWSSonnet
        Args:
            inputs (AWSSonnetInput): AWSSonnetInput object

        Returns:
            AWSSonnetOutput: AWSSonnetOutput object
        """
        response = self._inference_by_llm(
            inputs.user_prompt,
            inputs.system_prompt,
            inputs.json_mode,
        )
        return AWSSonnetOutput(response=response)

    def _create_user_message(self, user_prompt: str) -> list[dict]:
        """Create user message with given prompt

        Args:
            user_prompt (str): user prompt
        Returns:
            list: user message
        """
        return [
            {
                'role': 'user',
                'content': [
                    {
                        'text': user_prompt,
                    },
                ],
            },
        ]

    def _create_system_message(self, system_prompt: str) -> list[dict]:
        """Create system message with given prompt

        Args:
            system_prompt (str): system prompt
        Returns:
            list: system message
        """
        return [
            {
                'text': system_prompt,
            },
        ]
