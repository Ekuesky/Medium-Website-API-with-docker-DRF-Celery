from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", default="DZl06uZHfZzAPQydw6TqF5H9lAL4G3LcjomPcZZIH8p8mPFc8Qo"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", default="mailhog")
EMAIL_PORT = os.getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "support@ayiekdev.space"
DOMAIN = os.getenv("DOMAIN")
SITE_NAME = "Authors Haven"

# Logging Configurations
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
