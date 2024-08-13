import pytest
from django.contrib.auth import get_user_model

from core_apps.profiles.models import Profile
from core_apps.profiles.serializers import ProfileSerializer
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.mark.django_db
def test_get_full_name(normal_user):
    # create profile for normal_user
    profile = Profile.objects.create(user=normal_user)
    serializer = ProfileSerializer(instance=profile)
    # check if the full_name is in the serializer.data
    assert 'full_name' in serializer.data
    assert 'about_me' in serializer.data
    assert 'phone_number' in serializer.data
    # check if the full_name is correct
    assert serializer.data['full_name'] == f"{normal_user.first_name} {normal_user.last_name}"

@pytest.mark.django_db
def test_get_profile_photo(normal_user):
    image = SimpleUploadedFile("profile.jpg", b"file_content", content_type='image/jpeg')
    profile = Profile.objects.create(user=normal_user,
                                     phone_number="+1234567890",
                                     about_me="Test bio",
                                     gender="Male",
                                     country="US",
                                     city="Test City",
                                     profile_photo = image)
    serializer = ProfileSerializer(instance=profile)
    # check if the profile_photo is in the serializer.data
    assert 'profile_photo' in serializer.data
    # check if the profile_photo is a valid URL
    assert serializer.data["profile_photo"] == profile.profile_photo.url