from django.db.models import Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import  get_object_or_404
from django.db import IntegrityError
from rest_framework import status

from .models import Promotion, Comment, Company, Category, PromotionFilter, CompanyFilter,LikePromotion
from .permissions import IsAuthor
from .serializers import (
    PromotionSerializer,
    CommentSerializer,
    CompanySerializer,
    CategorySerializer,
    PromotionCountSerializer,
)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PromotionFilter
    serializer_class = PromotionSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
    


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'article']

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthor]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(methods=['POST', 'DELETE'], detail=True)
    def comment(self, request, pk=None):
        promotion = self.get_object()
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, promotion=promotion)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            comment_id = request.data.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({'message': 'Comment deleted successfully.'})


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_class = CompanyFilter


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthor]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('title')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class PromotionCountView(viewsets.ViewSet):
    queryset = Category.objects.all()
    serializer_class = PromotionCountSerializer
    filter_backends = [DjangoFilterBackend]

    def list(self, request):
        queryset = self.queryset.annotate(promotions_count=Count('promotions'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    

class PostPromotionLike(APIView):
    def get(self, request, promotion_id):
        promotion = get_object_or_404(Promotion, id=promotion_id)
        try:
            like = LikePromotion.objects.create(promotion=promotion, user=request.user)
        except IntegrityError:
            like = LikePromotion.objects.filter(promotion=promotion, user=request.user).delete()
            data = {f"Лайк для {promotion_id} акции убрал пользователь {request.user.email}"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': f"лайк акции {promotion_id} поставил пользователь {request.user.email}"}
            return Response(data, status=status.HTTP_201_CREATED)
        

