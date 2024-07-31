import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "user_first_name", "article_title", "rating", "review"]
