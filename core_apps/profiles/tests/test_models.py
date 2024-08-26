import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
# create a test for profile representation
def test_profile_representation(normal_user):
    profile = Profile.objects.create(user=normal_user)
    assert str(profile) == f"{normal_user.first_name}'s Profile"


import pytest

from core_apps.profiles.models import Profile


@pytest.mark.django_db
def test_profile_follow(normal_user):
    profile1 = Profile.objects.create(user=normal_user)
    user2 = User.objects.create_user(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        password="Password123",
    )
    profile2 = Profile.objects.create(user=user2)
    # Act of following
    profile1.follow(profile2)

    assert profile2 in profile1.followers.all()
    assert profile1 in profile2.following.all()


@pytest.mark.django_db
def test_unfollow_profile(normal_user):
    profile1 = Profile.objects.create(user=normal_user)
    user2 = User.objects.create_user(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        password="Password123",
    )
    profile2 = Profile.objects.create(user=user2)
    # Act of following
    profile1.follow(profile2)
    # Act of unfollowing
    profile1.unfollow(profile2)

    assert profile2 not in profile1.followers.all()
    assert profile1 not in profile2.following.all()


@pytest.mark.django_db
def test_check_following_profile(normal_user):
    profile1 = Profile.objects.create(user=normal_user)
    user2 = User.objects.create_user(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        password="Password123",
    )
    profile2 = Profile.objects.create(user=user2)
    # Act of following
    profile1.follow(profile2)

    assert profile1.check_following(profile2)
