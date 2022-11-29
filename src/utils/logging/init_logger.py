from logging.config import dictConfig

from src.utils.logging.config import get_logging_config


def init_logger(
        is_debug: bool = False,
        name: str = '',
):
    logging_config = get_logging_config(name=name, is_debug=is_debug)
    dictConfig(logging_config)
