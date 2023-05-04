from rest_framework import serializers
from .models import Promotion,Comment,Company,Category

class PromotionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    class Meta:
        model = Promotion
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'user', 'article', 'text', 'created_at', 'updated_at', 'sub_comment')
        read_only_fields = ['article']


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    class Meta:
        model = Company
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    discounts = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = [{'title': product.title, 'slug': product.slug} for product in instance.products.all()]
        representation['pk'] = instance.pk  # добавляем pk
        return representation

    
class PromotionCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id',  'promotions', 'promotions_count')