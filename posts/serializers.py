from rest_framework import serializers
from .models import Promotion, Comment, Company, Category
from django.db import models
from users.models import User


class PromotionSerializer(serializers.ModelSerializer):
    get_likes = serializers.ReadOnlyField()
    
    class Meta:
        model = Promotion
        fields = ['name', 'description', 'price', 'discount', 'image', 'created_at', 'updated_at', 'time_discount','get_likes',]     



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CategoryProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = Promotion
        fields = ['title', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    products = CategoryProductSerializer(many=True, read_only=True)
    promotions_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'promotions_count', 'products']


class PromotionCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'promotions', 'promotions_count']




