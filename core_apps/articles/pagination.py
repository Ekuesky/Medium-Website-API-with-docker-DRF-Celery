from django.utils.translation import gettext_lazy as _
from rest_framework.pagination import PageNumberPagination


class ArticlePaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 30
