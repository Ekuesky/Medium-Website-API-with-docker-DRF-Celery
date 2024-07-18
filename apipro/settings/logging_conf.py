#Logging Configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'general.log',
            'maxBytes': 2048 * 1024,
            'backupCount': 5,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level':'DEBUG',
            'propagate': True
        }
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {message}',
            'style': '{' # translated to string.format()
        }
    }
}
