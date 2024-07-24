from .base import *
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env( "DJANGO_SECRET_KEY",
    default="#p2fa2szwtx_z=qmni2(zcuez4&0%r!$xhb95nr!x&)9f1v97t")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "support@digital.site"
DOMAIN = env("DOMAIN")
SITE_NAME = "Ayiek Sky"