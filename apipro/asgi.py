import os

from django.core.asgi import get_asgi_application

# TODO: change this to apipro.settings.prod in prod environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apipro.settings.local")

application = get_asgi_application()
