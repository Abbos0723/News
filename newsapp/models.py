from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_news', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = "Kategoriyalar"
        verbose_name = "Kategoriya"


class Region(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('region_news', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = "Hududlar"
        verbose_name = "Hudud"


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name="Qisqa tavsif")
    content = models.TextField(blank=True, verbose_name="Matn")
    image = models.ImageField(upload_to="image/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    count_views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('read_more', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = "Yangiliklar"
        verbose_name = "Yangilik"
        ordering = ['-created_at']


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_news', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = "Teglar"
        verbose_name = "Teg"
