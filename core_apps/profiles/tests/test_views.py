import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core_apps.profiles.models import Profile

User = get_user_model()


@pytest.mark.django_db
def test_profile_detail_api_view_get_queryset(normal_user):
    """Test that ProfileDetailAPIView returns the expected profile."""
    client = APIClient()
    url = reverse("my-profile")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=normal_user)
    # create a new profile
    Profile.objects.create(user=normal_user)
    url = reverse("my-profile")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(normal_user.profile.id)
    assert response.data["gender"] == str(normal_user.profile.gender)
    assert response.data["country"] == str(normal_user.profile.country.name)
    assert response.data["phone_number"] == str(normal_user.profile.phone_number)
    assert response.data["about_me"] == normal_user.profile.about_me
    assert response.data["twitter_handle"] == str(normal_user.profile.twitter_handle)


@pytest.mark.django_db
def test_update_profile_api_view(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    # create a new profile
    Profile.objects.create(user=normal_user)
    url = reverse("update-profile")
    data = {"country": "Benin", "phone_number": "+22898456321"}
    response = client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["country"] == data["country"]
    assert response.data["phone_number"] == data["phone_number"]


@pytest.mark.django_db
def test_followers_list_view(normal_user):
    # test for followers_list_view

    client = APIClient()
    url = reverse("followers")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=normal_user)
    # check with none existing profile
    url = reverse("followers")
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # create a new profile
    Profile.objects.create(user=normal_user)

    # create a new user and profile
    new_user = User.objects.create_user(
        first_name="John",
        last_name="Doe",
        email="testuser2@example.com",
        password="testuser2",
    )
    Profile.objects.create(user=new_user)
    # follow the new user

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


# test for following listview
@pytest.mark.django_db
def test_following_list_view(normal_user):
    client = APIClient()

    client.force_authenticate(user=normal_user)
    # check with none existing profile
    url = reverse("following", args=[normal_user.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # create a profile for normal_user
    Profile.objects.create(user=normal_user)

    url = reverse("following", args=[normal_user.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


# test for FollowAPIView
@pytest.mark.django_db
def test_follow_api_view(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    # create new_user and profile
    new_user = User.objects.create_user(
        first_name="John",
        last_name="Doe",
        email="testuser2@example.com",
        password="testuser2",
    )
    Profile.objects.create(user=new_user)
    # check for none existing profile
    url = reverse("follow", args=[new_user.id])
    response = client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # create profile for normal_user
    Profile.objects.create(user=normal_user)
    # follow the new user
    url = reverse("follow", args=[new_user.id])
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert normal_user.profile.check_following(new_user.profile) is True


@pytest.mark.django_db
def test_follow_yourself(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    Profile.objects.create(user=normal_user)
    url = reverse("follow", args=[normal_user.id])
    response = client.post(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
# follow an already followed user
def test_follow_already_followed_user(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    # create new_user and profile
    new_user = User.objects.create_user(
        first_name="John",
        last_name="Doe",
        email="testuser2@example.com",
        password="testuser2",
    )
    Profile.objects.create(user=new_user)

    # create profile for normal_user
    Profile.objects.create(user=normal_user)

    # follow the new user
    url = reverse("follow", args=[new_user.id])
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK

    # try to follow the same user again
    url = reverse("follow", args=[new_user.id])
    response = client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
