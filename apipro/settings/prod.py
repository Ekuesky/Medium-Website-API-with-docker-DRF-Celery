from .base import *  # noqa

# ADMIN CONFIGURATION
# --------------------------------------------------------------------------------
ADMINS = [("Ayiek Sky", "ayiekdev.space")]

# SECURITY CONFIGURATION
# --------------------------------------------------------------------------------
# Liste des origines de confiance pour CSRF - Nécessaire pour la sécurité en production
CSRF_TRUSTED_ORIGINS = ["https://ayiekdev.space"]

# Configuration des paramètres critiques de sécurité
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")  # Clé secrète obligatoire en production
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY must be set in the environment.")

# Liste des hôtes autorisés - Crucial pour la sécurité en production
allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", default="localhost").split(",")
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts if host.strip()]

ADMIN_URL = os.getenv("DJANGO_ADMIN_URL")

# SSL/HTTPS CONFIGURATION
# --------------------------------------------------------------------------------
# Configurations SSL/HTTPS - Essentielles pour la sécurité en production
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # Important si derrière un proxy
SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", default=True)  # Force HTTPS

# Configuration des cookies sécurisés - Obligatoire en production avec HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Configuration HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 518400  # Durée HSTS - Protection contre les attaques downgrade

SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default="True"
).lower() == "true"

SECURE_CONTENT_TYPE_NOSNIFF = os.getenv(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default="True"
).lower() == "true"

# STATIC FILES CONFIGURATION
# --------------------------------------------------------------------------------
# Configuration de Whitenoise pour servir les fichiers statiques en production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# EMAIL CONFIGURATION
# --------------------------------------------------------------------------------
# Configuration des emails par défaut
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

# Configuration email avec Celery+Mailgun - Critique pour les notifications
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_HOST_USER = "postmaster@mg.ayiekdev.space"
EMAIL_HOST_PASSWORD = os.getenv("SMTP_MAILGUN_PASSWORD")  # À définir dans les variables d'environnement
EMAIL_PORT = os.getenv("EMAIL_PORT", default=587)
EMAIL_USE_TLS = True
DOMAIN = os.getenv("DOMAIN")

# LOGGING CONFIGURATION
# --------------------------------------------------------------------------------
# Configuration du logging - Important pour le debugging en production
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
        "mail_admins": {  # Envoi des erreurs par email aux administrateurs
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {  # Logging dans la console
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {  # Gestion des erreurs de requêtes
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {  # Gestion des tentatives d'accès non autorisées
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}