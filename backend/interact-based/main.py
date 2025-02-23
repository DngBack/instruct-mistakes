from __future__ import annotations

from contextlib import asynccontextmanager

from api.routes import interact_based_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.logging import get_logger
from shared.logging import setup_logging
from starlette.responses import RedirectResponse

setup_logging(json_logs=True)
logger = get_logger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = logger
    yield


app = FastAPI(
    title="Information Extraction API - Enfit AI",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def index():
    """Redirect to docs page

    Returns:
        RedirectResponse: docs page
    """
    return RedirectResponse(url="/docs")


# add middleware to generate correlation id
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add the routers
app.include_router(
    interact_based_router,
)
