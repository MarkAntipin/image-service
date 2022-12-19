import logging
import time
import typing as tp

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from settings import app_settings

logger = logging.getLogger(app_settings.TITLE)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: FastAPI,
            skip_paths: tp.Optional[tp.Sequence] = None
    ):
        super().__init__(app)
        if skip_paths is None:
            self.skip_paths = {'/docs', '/openapi.json', '/readyz', '/healthz', '/metrics'}
        else:
            self.skip_paths = skip_paths

    async def dispatch(self, request: Request, call_next):
        path = request.scope['path']
        start_time = time.perf_counter()

        response = await call_next(request)
        if path in self.skip_paths:
            return response

        request_duration = time.perf_counter() - start_time

        logger.info(
            'Request',
            extra={
                'request': {
                    'duration_ms': request_duration * 1000,
                    'uri': path,
                    'method': request.method,
                    'response_status': response.status_code,
                }
            }
        )
        return response
