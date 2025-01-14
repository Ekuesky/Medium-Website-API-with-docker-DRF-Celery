from .base import *  # noqa


ADMINS = [("Ayiek Sky", "ayiekdev.space")]

# TODO add domain names of the production server
CSRF_TRUSTED_ORIGINS = ["https://ayiekdev.space"]

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
  raise ValueError("DJANGO_SECRET_KEY must be set in the environment.")

allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", default="localhost").split(",")
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts if host.strip()]


ADMIN_URL = os.getenv("DJANGO_ADMIN_URL")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", default=True)

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# TODO: change to 518400 later
SECURE_HSTS_SECONDS = 518400

SECURE_HSTS_INCLUDE_SUBDOMAINS =os.getenv(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default="True"
).lower() == "true"

SECURE_CONTENT_TYPE_NOSNIFF = os.getenv(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default="True"
).lower() == "true"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_FROM_EMAIL = os.getenv(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Authors Haven Support <support@ayiekdev.space>",
)

SITE_NAME = "Authors Haven"

SERVER_EMAIL = os.getenv("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

EMAIL_SUBJECT_PREFIX = os.getenv(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Authors Haven]",
)

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_HOST_USER = "postmaster@mg.ayiekdev.space"
EMAIL_HOST_PASSWORD = os.getenv("SMTP_MAILGUN_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DOMAIN = os.getenv("DOMAIN")


# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
