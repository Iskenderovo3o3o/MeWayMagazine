from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
import django_filters

User = get_user_model()


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/images/promotions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_discount = models.DurationField(default=timedelta(days=7))

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sub_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    article = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.user.username}'


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock_count = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=80, unique=True)
    promotions_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class PromotionCount(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='promotions')
    product = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='promotions')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = not bool(self.pk)
        super().save(*args, **kwargs)
        if is_new:
            self.category.promotions_count += 1
            self.category.save()


class PromotionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Promotion
        fields = ['name']


class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    discount = django_filters.RangeFilter()

    class Meta:
        model = Company
        fields = ['name', 'discount']

