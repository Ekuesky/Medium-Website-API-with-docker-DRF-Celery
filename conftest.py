import pytest
from pytest_factoryboy import register
from core_apps.users.tests.factories import UserFactory
# for serializers
from django.test import RequestFactory
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware


register(UserFactory)

@pytest.fixture
def normal_user(db,user_factory):
    new_user = user_factory.create()
    return new_user

@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_staff=True, is_superuser=True)
    return new_user


@pytest.fixture
def mock_request():
    """
    Creates a mocked Django request object with a simulated session and authentication.

    This fixture allows you to test your code that depends on session or
    authentication functionality without making real requests or needing
    a fully configured Django application.
    """
    # Create a RequestFactory for building fake requests.
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