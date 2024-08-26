import pytest
from django.contrib.auth import get_user_model

# get the current user instance
User = get_user_model()


@pytest.mark.django_db
def test_create_normal_user(normal_user):
    assert normal_user.first_name is not None
    assert normal_user.last_name is not None
    assert normal_user.email is not None
    assert normal_user.password is not None
    assert normal_user.is_staff is False
    assert normal_user.is_active is True
    assert normal_user.is_superuser is False
    assert normal_user.pkid is not None


@pytest.mark.django_db
def test_create_superuser(super_user):
    assert super_user.first_name is not None
    assert super_user.last_name is not None
    assert super_user.email is not None
    assert super_user.password is not None
    assert super_user.is_staff is True
    assert super_user.is_active is True
    assert super_user.is_superuser is True
    assert super_user.pkid is not None


@pytest.mark.django_db
def test_get_full_name(normal_user):
    full_name = normal_user.get_full_name
    expected_full_name = (
        f"{normal_user.first_name.title()} {normal_user.last_name.title()}"
    )
    assert full_name == expected_full_name


@pytest.mark.django_db
def test_get_short_name(normal_user):
    short_name = normal_user.get_short_name
    assert short_name == normal_user.first_name


@pytest.mark.django_db
def test_user_str(normal_user):
    assert str(normal_user) == f"{normal_user.first_name}"


@pytest.mark.django_db
def test_create_user_with_no_lastname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "The user must have a last name."


@pytest.mark.django_db
def test_create_user_with_no_firstname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "The user must have a first name."


@pytest.mark.django_db
def test_create_user_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "The user must have an email address."


@pytest.mark.django_db
def test_create_superuser_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "The user must have an email address."


@pytest.mark.django_db
def test_create_superuser_with_no_password(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Superuser must have a password."


@pytest.mark.django_db
def test_super_user_is_not_staff(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(err.value) == "Superuser must have is_staff=True."


@pytest.mark.django_db
def test_super_user_is_not_superuser(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(err.value) == "Superuser must have is_superuser=True."


@pytest.mark.django_db
def test_update_user(normal_user):
    newfn = "John"
    newln = "Doe"

    normal_user.first_name = newfn
    normal_user.last_name = newln
    normal_user.save()

    updated_user = User.objects.get(pk=normal_user.pk)
    assert updated_user.first_name == newfn
    assert updated_user.last_name == newln


@pytest.mark.django_db
def test_delete_user(normal_user):
    normal_user.delete()
    assert not User.objects.filter(pk=normal_user.pk).exists()


@pytest.mark.django_db
def test_normalize_email(normal_user):
    email = normal_user.email
    normalized_email = normal_user.email.lower()
    assert email == normalized_email


@pytest.mark.django_db
def test_create_user_with_wrong_email(user_factory):
    # try to create a new user with the wrong email
    with pytest.raises(ValueError) as err:
        user_factory.create(email="testexample.com")
    assert str(err.value) == "You must provide a valid email address"
