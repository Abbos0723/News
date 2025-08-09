from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_list_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from .models import New, Category
from .forms import ContactForm, CommentForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from config.coustom_permissions import OnlyLoggedSuperUser
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm
from hitcount.views import HitCountDetailView, HitCountMixin


def news_list(request):
    news_list = New.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)


class NewsDetailView(FormMixin, DetailView):
    model = New
    template_name = "news/news_detail.html"
    context_object_name = "news"
    form_class = CommentForm

    def get_success_url(self):
        return self.request.path  # yoki: reverse('news_detail_page', kwargs={'news': self.get_object().slug})

    def get_queryset(self):
        # faqat Published yangiliklarni ko‘rsatamiz
        return New.object.filter(status=New.Status.Published)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_object()
        comments = news.comments.filter(active=True)
        context['comments'] = comments

        # Agar POST bo'lmasa, CommentFormni bo'sh holatda yuboramiz
        if 'comment_form' not in context:
            context['comment_form'] = self.get_form()
        context['new_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.news = self.object
            new_comment.user = request.user
            new_comment.save()

            # Success URLga redirect qilamiz
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(comment_form=form))


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


def news_detail(request, news):
    news = get_object_or_404(New, slug=news, status=New.Status.Published)
    context = {}
    # hitcount logikasi
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_conted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi koment yaratamiz lekin MB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # Izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            return redirect('news_detail_page', news=news.slug)
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        "comments": comments,
        "comment_form": comment_form,
        "new_comment": new_comment,
        "comment_count": comment_count

    }
    return render(request, "news/news_detail.html", context)


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


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = New
    fields = ('title', 'body', 'category', 'image', 'status', )
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = New
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = New
    template_name = 'crud/news_create.html'
    fields = ('title', 'title_uz', 'title_ru', 'title_en', 'slug', 'body', 'body_uz', 'body_ru', 'body_en', 'category', 'image', 'status', )

# class NewsCreateView(OnlyLoggedSuperUser, CreateView):
#   model = New
# fields = ('title', 'slug', 'body', 'category', 'image', 'status', )

#    def test_func(self):
#        return self.request.user.is_superuser


@login_required()
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = New
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return New.object.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )