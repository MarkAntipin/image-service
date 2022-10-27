from logging import getLogger

from fastapi import FastAPI
from backend_utils.server import register_routers

from api.routes.v1.app import compiled_routers as v1_routers
from settings import get_settings


logging = getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
    )
    register_routers(
        app=app,
        routers=[*v1_routers]
    )

    return app