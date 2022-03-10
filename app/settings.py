import os

PARSE_INTERVAL = int(os.getenv('CYRB_PARSE_INTERVAL', '60'))
LOG_LEVEL = os.getenv('CYRB_LOG_LEVEL', 'INFO')
SHOW_MAX = int(os.getenv('CYRB_SHOW_MAX', '10'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname).1s [%(name)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': False,
            'level': LOG_LEVEL,
        },
    },
}