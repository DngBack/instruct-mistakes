from __future__ import annotations

from api.helpers.exception_handler import ExceptionHandler
from api.helpers.exception_handler import ResponseMessage
from application import InteractBasedInput
from application import InteractBasedService
from fastapi import APIRouter
from fastapi import status
from shared.logging import get_logger

interact_based_router = APIRouter(prefix='/v1')
logger = get_logger(__name__)


@interact_based_router.post(
    '/prompting_interact_based/',
    response_model=str,
    tags=['interact_based'],
    responses={
        status.HTTP_200_OK: {
            'content': {},
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: ExceptionHandler.create_response_message(  # type: ignore
            ResponseMessage.INTERNAL_SERVER_ERROR,
        ),
        status.HTTP_400_BAD_REQUEST: ExceptionHandler.create_response_message(
            ResponseMessage.BAD_REQUEST,
        ),
        status.HTTP_401_UNAUTHORIZED: ExceptionHandler.create_response_message(
            ResponseMessage.INVALID_API_KEY,
        ),
        status.HTTP_402_PAYMENT_REQUIRED: ExceptionHandler.create_response_message(  # type: ignore
            ResponseMessage.UNPROCESSABLE_ENTITY,
        ),
    },
)
async def send_questions_answer(
    user_answer: str,
    correct_answer: str,
    exercies_type: str,
):
    """
    Processes the user's answer, compares it with the correct answer, and handles it based on the exercise type.

    Args:
        user_answer (str): The answer provided by the user.
        correct_answer (str): The correct answer.
        exercies_type (str): The type of exercise.

    Returns:
        str: The response from the interaction-based processing service.
    """
    exception_handler = ExceptionHandler(
        logger=logger.bind(),
        service_name='interact_based',
    )

    try:
        docs_sync_process = InteractBasedService()
        response = docs_sync_process.process(
            inputs=InteractBasedInput(
                user_answer=user_answer,
                correct_answer=correct_answer,
                exercies_type=exercies_type,
            ),
        )
        return response.response

    except Exception:
        return exception_handler.handle_exception(
            message=ResponseMessage.INTERNAL_SERVER_ERROR,
            extra={
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'exercies_type': exercies_type,
            },
        )


@interact_based_router.get('/healthz', tags=['infor_extractor'])
async def healthz():
    return {'status': 'ok'}
