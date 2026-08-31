import logging
from pythonjsonlogger.json import JsonFormatter


def setup_logger(module_name: str, log_level: int = logging.INFO) -> logging.Logger:
    """Настройка логгера для модуля."""

    logger_instance = logging.getLogger()
    logger_instance.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter(
        ['levelname', 'message', 'asctime'],
        defaults={
            'service': 'education_platform_api',
            'module': module_name,
            'version': '1.0.0',
        },
    ))
    logger_instance.addHandler(handler)

    return logger_instance
