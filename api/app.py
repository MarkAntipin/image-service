from logging import getLogger

from backend_utils.server import register_routers
from fastapi import FastAPI

from api.routes.v1.app import compiled_routers as v1_routers
from settings import settings

logging = getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
    )
    register_routers(
        app=app,
        routers=[*v1_routers]
    )

    return app
