from __future__ import annotations

import time

import structlog
from asgi_correlation_id.context import correlation_id
from fastapi import Request
from fastapi import Response
from starlette.websockets import Message
from uvicorn.protocols.utils import get_path_with_query_string


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


async def logging_middleware(request: Request, call_next) -> Response:
    structlog.contextvars.clear_contextvars()
    # These context vars will be added to all
    # log entries emitted during the request

    logger = request.app.state.logger
    request_id = correlation_id.get()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter_ns()
    response = Response(status_code=500)

    try:
        await set_body(request, await request.body())
        body = await get_body(request)
        response = await call_next(request)
    except Exception:
        structlog.stdlib.get_logger(
            "api.error",
        ).exception("Uncaught exception")
        raise
    finally:
        process_time = time.perf_counter_ns() - start_time
        status_code = response.status_code
        url = get_path_with_query_string(request.scope)
        client_host = request.client.host
        client_port = request.client.port
        http_method = request.method
        http_version = request.scope["http_version"]

        # Recreate the Uvicorn access log format,
        # but add all parameters as structured information
        logger.info(
            f"""{client_host}:{client_port} - "{http_method} \
            {url} HTTP/{http_version}" {status_code}""",
            http={
                "url": str(request.url),
                "status_code": status_code,
                "method": http_method,
                "request_id": request_id,
                "version": http_version,
                "body": body,
            },
            duration=process_time,
        )
        response.headers["X-Process-Time"] = str(process_time / 10**9)
        return response
