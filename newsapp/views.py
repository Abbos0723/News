from django.shortcuts import render, get_object_or_404
from django.db.models import F
from newsapp.models import *


def home(request):
    context = {
        "news": News.objects.order_by("-created_at")
    }
    return render(request, "newsapp/home.html", context)


def category_news(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news = News.objects.filter(category=category)
    context = {
        'category': category,
        'news': news,
    }
    return render(request, "newsapp/category_news.html", context)


def region_news(request, slug):
    region = get_object_or_404(Region, slug=slug)
    news = News.objects.filter(region=region)
    context = {
        'region': region,
        'news': news,
    }
    return render(request, "newsapp/region_news.html", context)


def read_more(request, slug):
    new = get_object_or_404(News, slug=slug)
    most_viewed = News.objects.order_by('-count_views')
    News.objects.filter(pk=new.pk).update(count_views=F('count_views') + 1)

    context = {
        'new': new,
        'most_viewed': most_viewed,
    }
    return render(request, "newsapp/read_more.html", context)


def tag_news(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    tag_news = News.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'tag_news': tag_news,
    }
    return render(request, "newsapp/tag_news.html", context)