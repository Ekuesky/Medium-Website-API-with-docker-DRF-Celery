import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# CORE CONFIGURATION
# --------------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = os.path.join(ROOT_DIR, "core_apps")

# ENVIRONMENT SETUP
# --------------------------------------------------------------------------------
# TODO: Change this in production
env_file = os.path.join(ROOT_DIR, ".envs", ".env.local")
if os.path.isfile(env_file):
    load_dotenv(env_file)

DEBUG = os.getenv("DJANGO_DEBUG", False)

# APPLICATIONS CONFIGURATION
# --------------------------------------------------------------------------------
DJANGO_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_APPS = [
    "django_prometheus",
    # REST Framework
    "rest_framework",
    "django_filters",
    "corsheaders",

    # Utilities
    "django_countries",
    "phonenumber_field",
    "taggit",

    # Documentation
    "drf_yasg",

    # Email
    "djcelery_email",

    # Authentication
    "allauth",
    "allauth.account",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",

    # Search
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.users",
    "core_apps.profiles",
    "core_apps.articles",
    "core_apps.ratings",
    "core_apps.bookmarks",
    "core_apps.responses",
    "core_apps.search",

]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# --------------------------------------------------------------------------------
MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# TEMPLATES CONFIGURATION
# --------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# DATABASE CONFIGURATION
# --------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

# PASSWORD CONFIGURATION
# --------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]

# INTERNATIONALIZATION
# --------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lome"
USE_I18N = True
USE_TZ = True
SITE_ID = 1

# STATIC AND MEDIA FILES CONFIGURATION
# --------------------------------------------------------------------------------
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(ROOT_DIR, "mediafiles")

# ADMIN CONFIGURATION
# --------------------------------------------------------------------------------
ADMIN_URL = "hidden/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

# CELERY CONFIGURATION
# --------------------------------------------------------------------------------
CELERY_BROKER_URL = os.getenv("CELERY_BROKER")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_TASK_SEND_SENT_EVENT = True

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

# REST FRAMEWORK CONFIGURATION
# --------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["dj_rest_auth.jwt_auth.JWTCookieAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

CORS_URLS_REGEX = r"^/api/.*$"

ALLOWED_HOSTS =["*"]
# JWT CONFIGURATION
# --------------------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": os.getenv("SIGNING_KEY"),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# AUTHENTICATION CONFIGURATION
# --------------------------------------------------------------------------------
REST_AUTH = {
    "REGISTER_SERIALIZER": "core_apps.users.serializers.CustomRegisterSerializer",
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "apipro-access-token",
    "JWT_AUTH_REFRESH_COOKIE": "apipro-refresh-token",
}

AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

# ELASTICSEARCH CONFIGURATION
# --------------------------------------------------------------------------------
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": "es:9200",
    },
}

# PROMETHEUS CONFIGURATION
# --------------------------------------------------------------------------------
# Disable auto-export of metrics to avoid port binding issues
PROMETHEUS_EXPORT_METRICS = False

# URLs CONFIGURATION
# --------------------------------------------------------------------------------
ROOT_URLCONF = "apipro.urls"
WSGI_APPLICATION = "apipro.wsgi.application"