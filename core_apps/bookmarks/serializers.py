from rest_framework import serializers

from core_apps.bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    user_fname = serializers.CharField(source="user.firstname", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "user_fname", "article_title", "created_at"]
        read_only_fields = ["user"]
