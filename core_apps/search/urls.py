# import path
from django.urls import path

# import views
from .views import  ArticleElasticSearchView

urlpatterns = [
    path("search/", ArticleElasticSearchView.as_view({"get": "list"}), name="article-search"),
]