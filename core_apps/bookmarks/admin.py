from django.contrib import admin
from .models import Bookmark

# Register your models here.


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'article']
    list_display_links = ['id', 'user']
    list_filter = ['id', 'user']


admin.site.register(Bookmark, BookmarkAdmin)

