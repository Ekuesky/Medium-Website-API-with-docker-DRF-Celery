from django.urls import path
from .views import ResponseListCreateView, ResponseDetailView



urlpatterns = [
    path("response/<uuid:article_id>/", ResponseListCreateView.as_view(), name="response-list-create"),
    path("<uuid:id>/", ResponseDetailView.as_view(), name="response-detail"),
]