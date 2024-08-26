from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404

from .models import Article, Response
from .serializers import ResponseSerializer


class ResponseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResponseSerializer
    queryset = Response.objects.all()

    def get_queryset(self):
        # get article from url
        article_id = self.kwargs.get("article_id")
        return Response.objects.filter(article__id=article_id, parent_response=None)

    def perform_create(self, serializer):
        user = self.request.user
        # get article_id from url
        article_id = self.kwargs.get("article_id")
        # check if article exists in database and required constraint
        article = get_object_or_404(Article, id=article_id)
        serializer.save(article=article, user=user)


class ResponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResponseSerializer
    queryset = Response.objects.all()
    lookup_field = "id"

    def perform_update(self, serializer):
        user = self.request.user
        response = self.get_object()
        # check if user is the owner of the response
        if response.user != user:
            raise PermissionDenied("You are not the owner of this response.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        response = self.get_object()
        # check if user is the owner of the response
        if response.user != user:
            raise PermissionDenied("You are not the owner of this response.")
        instance.delete()
