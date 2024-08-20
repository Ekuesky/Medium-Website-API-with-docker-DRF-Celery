from django.conf import settings
from django.db import models

from core_apps.articles.models import Article


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ["user", "article"]

    def __str__(self):
        return f"{self.user.first_name} bookmarked {self.article.title}"

