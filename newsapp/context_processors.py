from newsapp.models import Category, Region, News


def category(request):
    categories = Category.objects.all()
    return {'categories': categories}


def regions(request):
    regions = Region.objects.all()
    return {'regions': regions}


def latest_news(request):
    latest_news = News.objects.order_by("-created_at")
    return {'latest_news': latest_news}