from fastapi import FastAPI
from src.core.settings import get_settings
from src.core.exceptions import (
    AppException,
    app_exception_handler,
)
from src.core.logger import setup_logger
from src.api.v1.routers import v1_router

setup_logger()

settings = get_settings()

app = FastAPI()

src.add_exception_handler(AppException, app_exception_handler)

src.include_router(v1_router, prefix='/api')