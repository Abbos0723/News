from django.contrib import admin
from .models import New, Category, Contact, Comment


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


@admin.register(Comment)        # 2-usul
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'activate_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)

# 1-usul
# admin.site.register(Comment, CommentAdmin)