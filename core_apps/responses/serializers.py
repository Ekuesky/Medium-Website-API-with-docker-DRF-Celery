from rest_framework import serializers

from .models import Response


class ResponseSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Response
        fields = [
            "id",
            "user_first_name",
            "article_title",
            "content",
            "parent_response",
            "created_at",
        ]
