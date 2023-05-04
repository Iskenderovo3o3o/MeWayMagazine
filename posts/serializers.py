from rest_framework import serializers
from .models import Promotion, Comment, Company, Category


class PromotionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Promotion
        fields = ['name', 'description', 'price', 'discount', 'image', 'created_at', 'updated_at', 'time_discount']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'article', 'text', 'created_at', 'updated_at', 'sub_comment']
        read_only_fields = ['article']


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
