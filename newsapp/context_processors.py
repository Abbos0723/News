from newsapp.models import Category, Region, News


def category(request):
    return {'categories': Category.objects.all()}


def regions(request):
    return {'regions': Region.objects.all()}


def latest_news(request):
    return {'latest_news': News.objects.order_by("-created_at")[:10]}