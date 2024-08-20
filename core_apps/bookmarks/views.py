from rest_framework import generics, permissions, status
from rest_framework.response import Response

from.models import Bookmark
from.serializers import BookmarkSerializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from core_apps.articles.models import Article
from uuid import UUID


class BookmarkCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def perform_create(self, serializer):
        #get article_id from url
        article_id = self.kwargs.get("article_id")
        # check if article exists in database and required constraint
        if article_id:
            # get article object from database based on provided article_id
            # if article does not exist, raise ValidationError
            # if article exists, save bookmark with user and article reference in serializer.save() method below
            # serializer.save() method will save bookmark object in database and return it
            # if bookmark already exists for this user and article, raise ValidationError
            # note: this validation is done in serializer.save() method in serializers.py, not here.
            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                raise ValidationError("Invalid article id provided")
        else:
            raise ValidationError("article_id is required")
        # check if bookmark already exists for this user and article
        try:
            serializer.save(user=self.request.user, article=article)
        except IntegrityError:
            raise ValidationError("You have already bookmarked this article")


class BookmarkDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Bookmark.objects.all()

    # Identify article from URL by "article_id"
    lookup_field = "article_id"

    # Implement get_object method to get the object the current user can  delete
    def get_object(self):
        article_id = self.kwargs.get("article_id")
        try:
            UUID(str(article_id), version=4)
            bookmark = Bookmark.objects.get(user=self.request.user, article__id=article_id)
            return bookmark
        except Bookmark.DoesNotExist:
            raise NotFound("Bookmark not found")
        except ValueError:
            raise ValidationError("Invalid bookmark id provided")

    def perform_destroy(self, instance):
        user = self.request.user
        if user!= instance.user:
            raise ValidationError("You can only delete your own bookmarks")
        instance.delete()


