from django.contrib import admin
from .models import New, Category, Contact


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "publish_time", "status")
    list_filter = ("status", "create_time", "publish_time")
    prepopulated_fields = {"slug": ('title',)}
    search_fields = ["title", "body"]
    date_hierarchy = "publish_time"
    ordering = ["status", "publish_time"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(Contact)