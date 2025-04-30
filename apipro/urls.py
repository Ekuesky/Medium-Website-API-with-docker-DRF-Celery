from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core_apps.users.views import CustomUserDetailsView

schema_view = get_schema_view(
    openapi.Info(
        title="Make an API like a pro",
        default_version="v1",
        description="API endpoints for Api like a pro Course",
        contact=openapi.Contact(email="apipro@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
admin_url = getattr(settings, 'ADMIN_URL', 'admin/')
if admin_url == "None" or admin_url is None:
    admin_url = 'admin/'

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path(admin_url, admin.site.urls, name="admin"),
    path("api/v1/auth/user/", CustomUserDetailsView.as_view(), name="user_details"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "api/v1/auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/articles/", include("core_apps.articles.urls")),
    path("api/v1/ratings/", include("core_apps.ratings.urls")),
    path("api/v1/bookmarks/", include("core_apps.bookmarks.urls")),
    path("api/v1/responses/", include("core_apps.responses.urls")),
    path("api/v1/elastic/", include("core_apps.search.urls")),
    path('metrics/', include('django_prometheus.urls'))
]
# for pattern in urlpatterns:
#     print(f"Checking pattern: {pattern}")
#     if hasattr(pattern, 'urlconf_name'):
#         print(f"URLconf module: {pattern.urlconf_name}")

admin.site.site_header = "Authors heaven"

admin.site.site_title = "Authors heaven"

admin.site.index_title = "Welcome to authors Portal"
