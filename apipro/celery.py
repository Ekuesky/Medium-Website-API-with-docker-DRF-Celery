import os  # Import the os module to interact with the operating system

from celery import Celery  # Import the Celery class from the celery library
from django.conf import settings  # Import the settings object from Django

# TODO: Change this in production
# Set the default Django settings module for the Celery application
# This is necessary for Celery to know which Django settings to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apipro.settings.local")

# Create a new Celery application instance named "apipro"
app = Celery("apipro")

# Load configuration settings from the Django settings file
# The 'namespace' parameter ensures that all Celery-related settings keys
# are prefixed with 'CELERY_' in the Django settings fil, to avoid clashes
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks from all installed apps listed in Django's INSTALLED_APPS
# This lambda function ensures that Celery looks for a 'tasks.py' file in each app directory
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
