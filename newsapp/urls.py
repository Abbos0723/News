from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path("category/<slug:slug>", category_news, name="category_news"),
    path("region/<slug:slug>", region_news, name="region_news"),
    path("read_more/<slug:slug>", read_more, name="read_more"),
    path("tag/<slug:slug>", tag_news, name="tag_news"),
]
