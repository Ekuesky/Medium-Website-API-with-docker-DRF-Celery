import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from core_apps.users.serializers import CustomRegisterSerializer, UserSerializer

User = get_user_model()


@pytest.mark.django_db
def test_user_serializer_valid_data(normal_user):
    serializer = UserSerializer(instance=normal_user)
    assert "id" in serializer.data
    assert "gender" in serializer.data
    assert "email" in serializer.data
    assert "phone_number" in serializer.data
    assert "profile_photo" in serializer.data
    assert "country" in serializer.data
    assert "first_name" in serializer.data
    assert "last_name" in serializer.data
    assert "city" in serializer.data


@pytest.mark.django_db
def test_custom_register_serializer_valid_data(mock_request):
    # check the serializer with valid(email, first_name, last_name, password1, password2) and invalid data
    data = {
        "email": "test@google.com",
        "first_name": "John",
        "last_name": "Doe",
        "password1": "Test_password1",
        "password2": "Test_password1",
    }
    serializer = CustomRegisterSerializer(data=data)
    assert serializer.is_valid()

    user = serializer.save(mock_request)
    assert isinstance(user, User)
    assert user.email == "test@google.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"


@pytest.mark.django_db
def test_custom_register_serializer_invalid_data():
    # check the serializer with invalid(email, first_name, last_name, password1, password2) data
    data = {
        "email": "test@google.com",
        "first_name": "John",
        "last_name": "Doe",
        "password1": "Test_password1",
        "password2": "Test_password2",
    }
    serializer = CustomRegisterSerializer(data=data)
    assert not serializer.is_valid()
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_to_representation_normal_user(normal_user):
    # check "admin" is not in serializer.data
    serializer = UserSerializer(instance=normal_user)
    assert "admin" not in serializer.data


@pytest.mark.django_db
def test_to_representation_admin_user(super_user):
    # check "admin" is in serializer.data
    serializer = UserSerializer(instance=super_user)
    assert "admin" in serializer.data
