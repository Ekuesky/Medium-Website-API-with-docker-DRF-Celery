from rest_framework.pagination import PageNumberPagination
from django.utils.translation import gettext_lazy as _


class ArticlePaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 30