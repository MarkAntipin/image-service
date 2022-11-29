import logging

from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from settings import app_settings

logger = logging.getLogger(app_settings.TITLE)


class ErrorsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(
                e,
                extra={
                    'request': {
                        'uri': request.scope['path'],
                        'method': request.method,
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                    }
                },
                exc_info=True
            )
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content='Internal Server Error',
        )
