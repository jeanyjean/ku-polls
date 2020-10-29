import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },

    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },

    'loggers': {
        'polls': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },

    'formatters': {
        'simple': {
            'format': '%(asctime)s : %(message)s',
            'datefmt': '%d/%m/%Y %I:%M:%S %p', 
        },
    },
}