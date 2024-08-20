#import path from django.urls
from django.urls import path

from.views import BookmarkCreateView, BookmarkDeleteView

urlpatterns = [
    path("<uuid:article_id>/", BookmarkCreateView.as_view(), name="bookmark_article"),
    path("<uuid:article_id>", BookmarkDeleteView.as_view(), name="delete_bookmark"),
]

