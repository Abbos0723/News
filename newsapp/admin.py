from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name", )}


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name", )}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "category", "region", "created_at"]
    list_display_links = ['title', 'content']
    prepopulated_fields = {"slug": ("title", )}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name", )}