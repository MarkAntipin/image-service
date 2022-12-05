import logging
import traceback
import typing as tp
from datetime import datetime

from pydantic import BaseModel, Field


class RequestLog(BaseModel):
    uri: str
    method: str

    duration_ms: tp.Optional[int] = None

    response_status: tp.Optional[int] = None


class JsonLog(BaseModel):
    timestamp: str = Field(..., alias='@timestamp')
    app: tp.Optional[str]
    level: str
    message: str
    line_number: str

    error: tp.Optional[str] = None
    stacktrace: tp.Optional[str] = None

    request: tp.Optional[RequestLog] = None

    class Config:
        allow_population_by_field_name = True


class JSONLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        log_obj = self._make_log_object(record)
        return log_obj.json(exclude_unset=True, by_alias=True, exclude_none=True)

    @staticmethod
    def _make_log_object(record: logging.LogRecord) -> BaseModel:
        log_obj = JsonLog(
            timestamp=datetime.utcfromtimestamp(
                record.created
            ).isoformat() + 'Z',
            level=record.levelname.lower(),
            message=record.getMessage(),
            name=record.name,
            line_number=f'{record.pathname}:{record.lineno}'
        )

        if record.exc_info:
            e_type, value, tb = record.exc_info
            if value:
                log_obj.error = repr(value)
            if tb:
                log_obj.stacktrace = ''.join(traceback.format_exception(e_type, value, tb))

        if hasattr(record, 'request'):
            request = record.request
            request_log = RequestLog(
                uri=request['uri'],
                method=request['method'],
                duration_ms=request.get('duration_ms'),
                response_status=request.get('response_status'),
            )
            log_obj.request = request_log

        return log_obj
