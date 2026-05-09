from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404

from newsapp.models import Category, News, Region, Tag

PAGE_SIZE = 10


def _paginate(request, queryset):
    paginator = Paginator(queryset, PAGE_SIZE)
    return paginator.get_page(request.GET.get('page'))


def home(request):
    return render(request, "newsapp/home.html", {
        "page_obj": _paginate(request, News.objects.order_by("-created_at")),
    })


def category_news(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, "newsapp/category_news.html", {
        'category': category,
        'page_obj': _paginate(request, News.objects.filter(category=category)),
    })


def region_news(request, slug):
    region = get_object_or_404(Region, slug=slug)
    return render(request, "newsapp/region_news.html", {
        'region': region,
        'page_obj': _paginate(request, News.objects.filter(region=region)),
    })


def read_more(request, slug):
    new = get_object_or_404(News, slug=slug)
    News.objects.filter(pk=new.pk).update(count_views=F('count_views') + 1)
    return render(request, "newsapp/read_more.html", {
        'new': new,
        'most_viewed': News.objects.order_by('-count_views')[:10],
    })


def tag_news(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return render(request, "newsapp/tag_news.html", {
        'tag': tag,
        'page_obj': _paginate(request, News.objects.filter(tags=tag)),
    })