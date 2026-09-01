import logging
from pythonjsonlogger.json import JsonFormatter

from app.core.context import get_request_id


class ExtraAttributesFiler(logging.Filter):
    """Фильтр для добавления доп. полей."""

    def filter(self, record: logging.LogRecord) -> bool:
        request_id = get_request_id()

        if request_id:
            record.request_id = request_id
        else:
            record.request_id = None

        return True


def setup_logger(module_name: str, log_level: int = logging.INFO) -> logging.Logger:
    """Настройка логгера для модуля."""

    logger_instance = logging.getLogger(module_name)
    logger_instance.setLevel(log_level)

    if not logger_instance.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter(
            [
                'levelname',
                'message',
                'asctime',
                'request_id',
            ],
            defaults={
                'service': 'education_platform_api',
                'module': module_name,
                'version': '1.0.0',
            },
        ))
        logger_instance.addHandler(handler)
        logger_instance.addFilter(ExtraAttributesFiler())

    return logger_instance
