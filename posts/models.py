from datetime import timedelta
from django.contrib.auth import get_user_model
from slugify import slugify
import django_filters

from django.db import models

User = get_user_model()

class Promotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_discount = models.DurationField(default=timedelta(days=7))


    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акция'
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # не существующий коментарий
    updated_at = models.DateTimeField(auto_now=True) # существующий коментарий
    sub_comment = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null = True)# не обязательно к заполнению blank true
    article = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='comments')
    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
    def __str__(self) -> str:
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
        return self.title
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80, unique=True)
    promotions_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
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

    class Meta:
        model = Company
        fields = ['name']

    
