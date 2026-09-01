import uuid
import time
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.context import set_request_id
from app.core.logging import setup_logger


middleware_logger = setup_logger(__name__)


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        raw_request_id = request.headers.get('X-Request-ID')

        try:
            request_id = uuid.UUID(raw_request_id) if raw_request_id else uuid.uuid4()
        except (ValueError, TypeError):
            request_id = uuid.uuid4()

        set_request_id(request_id)

        start_time = time.perf_counter()
        middleware_logger.info(
            'Request started',
            extra={'method': request.method, 'path': request.url.path},
        )

        try:
            response = await call_next(request)
        finally:
            set_request_id(None)

        process_time = time.perf_counter() - start_time
        middleware_logger.info({'process_time': process_time})
        response.headers['X-Request-ID'] = str(request_id)

        return response
