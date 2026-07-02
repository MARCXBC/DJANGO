from django.contrib import admin
from .models import Blog, BlogImage


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display=(
        "id",
        "title",
        "author",
        "created_at"
    )

    search_fields=("title", "content")
    list_filter = ("created_at",)


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):

    list_display=(
        "id",
        "blog",
        "image",
    )

# Register your models here.
