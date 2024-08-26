import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

# For preventing automatic profile creation
from django.db.models.signals import post_save

# for serializers
from django.test import RequestFactory
from pytest_factoryboy import register

from core_apps.profiles.signals import create_user_profile
from core_apps.users.tests.factories import UserFactory

User = get_user_model()

register(UserFactory)


@pytest.fixture
def normal_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_staff=True, is_superuser=True)
    return new_user


@pytest.fixture
def mock_request():
    factory = RequestFactory()

    # Create a GET request to the root URL ('/').
    request = factory.get("/")

    # Simulate Session Middleware execution
    middleware = SessionMiddleware(lambda req: None)
    # Process the request, initializing session data (e.g., setting cookies)
    middleware.process_request(request)
    # Save session data to the database or session store.
    request.session.save()

    # Simulate Authentication Middleware execution
    auth_middleware = AuthenticationMiddleware(lambda req: None)
    # Process the request, potentially setting up user authentication data.
    auth_middleware.process_request(request)

    # Return the fully prepared mock request for use in your tests.
    return request


@pytest.fixture(scope="session", autouse=True)
def disconnect_profile_signal():
    post_save.disconnect(create_user_profile, sender=User)
    yield
    post_save.connect(create_user_profile, sender=User)
