from fastapi import FastAPI
from app.core.settings import get_settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
)
from app.core.logger import setup_logger
from app.api.v1.routers import v1_router

setup_logger()

settings = get_settings()

app = FastAPI()

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(v1_router, prefix='/api')