from django.contrib import admin

# Register your models here.
from . import models


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "author", "title", "slug", "view_count"]
    list_display_links = ["pkid", "author"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "body", "tags"]
    ordering = ["-created_at"]


class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ["pkid", "article", "user", "viewer_ip"]
    list_display_links = ["pkid", "article"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["article", "user", "viewer_ip"]


class ClapAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "article"]
    list_display_links = ["id", "user"]
    list_filter = ["created_at", "updated_at"]

admin.site.register(models.Clap, ClapAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleView, ArticleViewAdmin)
