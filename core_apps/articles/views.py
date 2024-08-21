import logging

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .filters import ArticleFilter
from .models import Article, ArticleView, Clap
from .pagination import ArticlePaginator
from .permissions import IsOwnerOrReadOnly
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .serializers import ArticleSerializer, ClapSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ArticlePaginator
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ArticleFilter
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    renderer_classes = [ArticlesJSONRenderer]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(
            f"article {serializer.data.get('title')} created by {self.request.user.first_name}"
        )


class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    renderer_classes = [ArticleJSONRenderer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)
        if "banner_image" in self.request.FILES:
            if (
                instance.banner_image
                and instance.banner_image.name != "/profile_default.png"
            ):
                default_storage.delete(instance.banner_image.path)
            instance.banner_image = self.request.FILES["banner_image"]
            instance.save()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            raise NotFound(
                {
                    "detail": "L'article avec cet ID n'existe pas.",
                    "code": "article_not_found",
                }
            )

            # return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)

        viewer_ip = request.META.get("REMOTE_ADDR", None)
        ArticleView.record_view(
            article=instance, user=request.user, viewer_ip=viewer_ip
        )

        return Response(serializer.data)

class ClapView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Clap.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClapSerializer

    def create(self, request, *args, **kwargs):
        # get article_id from url
        article_id = kwargs.get("article_id")
        # check if article exists in database and required constraint
        article = get_object_or_404(Article, id=article_id)
        # check if user has already clapped for this article
        if Clap.objects.filter(article=article, user=request.user).exists():
            return Response({"details":"You already clapped for this article"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            clap = Clap.objects.create(user=request.user, article=article)
            clap.save()
            return Response({"details":"Clap added successfully"}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        # get article_id from url
        article_id = kwargs.get("article_id")
        # check if article exists in database and required constraint
        article = get_object_or_404(Article, id=article_id)
        # check if user has already clapped for this article
        clap = Clap.objects.filter(article=article, user=request.user).first()
        if clap:
            clap.delete()
            return Response({"details":"Clap deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"details":"You have not clapped for this article"}, status=status.HTTP_404_NOT_FOUND)
