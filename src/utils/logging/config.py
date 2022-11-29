def get_logging_config(
        name: str = '',
        is_debug: bool = False
):
    handlers = ['default'] if is_debug else ['json']
    uvicorn_level = 'INFO' if is_debug else 'ERROR'
    level = 'DEBUG' if is_debug else 'INFO'
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': 'src.utils.logging.formatter.JSONLogFormatter',
            },
            'default': {
                '()': 'uvicorn.logging.DefaultFormatter',
                'fmt': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'json': {
                'formatter': 'json',
                # TODO: use 'asynclog.AsyncLogDispatcher' 'class' with 'sys.stdout.write' 'func'
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
            }
        },
        'loggers': {
            name: {
                'handlers': handlers,
                'level': level,
                'propagate': False,
            },
            'uvicorn': {
                'handlers': handlers,
                'level': uvicorn_level,
                'propagate': False,
            },
            'uvicorn.access': {
                'handlers': handlers,
                'level': uvicorn_level,
                'propagate': False,
            },
            'PIL.PngImagePlugin': {
                'handlers': handlers,
                'level': uvicorn_level,
                'propagate': False,
            }
        },
    }
