from django.shortcuts import render, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from .models import New, Category
from .forms import ContactForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


def news_list(request):
    news_list = New.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


def news_detail(request, news):
    news = get_object_or_404(New, slug=news, status=New.Status.Published)
    context = {
        "news": news
    }
    return render(request, "news/news_detail.html", context)


def homePageView(request):
    categories = Category.objects.all()
    news_list = New.published.all().order_by('-publish_time')[:10]
    news_mah_one = New.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[0]
    news_mah = New.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[1:6]
    context = {
        'categories': categories,
        'news_list': news_list,
        'news_mah_one': news_mah_one,
        'news_mah': news_mah,
    }
    return render(request, "news/home.html", context)


class HomePageView(ListView):
    model = New
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = New.published.all().order_by('-publish_time')[:4]
        context['news_mah_one'] = New.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[:5]
        context['news_xor_one'] = New.published.all().filter(category__name='Xorij').order_by('-publish_time')[:5]
        context['news_tex_one'] = New.published.all().filter(category__name='Texnologiya').order_by('-publish_time')[:5]
        context['news_spo_one'] = New.published.all().filter(category__name='Sport').order_by('-publish_time')[:5]

        return context

class ContactPageView(TemplateView):
    tamplate_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur</h2>")
        context = {
            "form": form
        }
        return render(request, "news/contact.html", context)


def Xato404PageView(request):
    context = {

    }
    return render(request, 'news/404.html', context)


def aboutPageView(request):
    context = {

    }
    return render(request, 'news/about.html', context)


class MahalliyNewsView(ListView):
    model = New
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Mahalliy")
        return news


class XorijiyNewsView(ListView):
    model = New
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij")
        return news


class TexnologiyaNewsView(ListView):
    model = New
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Texnologiya")
        return news


class SportNewsView(ListView):
    model = New
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport")
        return news


class NewsUpdateView(UpdateView):
    model = New
    fields = ('title', 'body', 'category', 'image', 'status', )
    template_name ='crud/news_edit.html'


class NewsDeleteView(DeleteView):
    model = New
    template_name ='crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(CreateView):
    model = New
    template_name ='crud/news_create.html'
    fields = ('title', 'slug', 'body', 'category', 'image', 'status', )