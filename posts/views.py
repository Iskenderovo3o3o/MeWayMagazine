from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Promotion, Comment,Company,Category,PromotionFilter,CompanyFilter
from .serializers import PromotionSerializer, CommentSerializer,CompanySerializer,CategorySerializer,PromotionCountSerializer
from rest_framework import mixins, permissions, viewsets
from .permissions import IsAuthor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PromotionFilter


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context

    def get_permissions(self):
        if self.request.method == 'POST': # если пользователь хочет сделать одно из эти действий то у него бкдет проверяться токен
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsAuthor] #обновлять и удалять может тольок автор 
        return super().get_permissions()
    

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated] #передан ли токен 
        elif self.action in ['update','destroy']:
            self.permission_classes = [IsAuthor]  # автор ли он коментария 
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    
    def get_serializer_class(self):
        if self.action == 'comment':
            return CommentSerializer
        return super().get_serializer_class()
    
    @action(methods=['POST','DELETE'],detail=True) #DETAIL TRUE ЗАПРАШИВАЕТ ID
    def comment(self,request,pk=None):
        article = self.get_object()# по pk получает статью к которой обращается 
        # Article.objects.get(pk=pk)
        if self.request.method == 'POST':
            serializer = CommentSerializer(data=request.data,context = {'request': request})
            serializer.is_valid(raise_exception=True)#правильные ли все входные данные
            serializer.save(user=request.user,article=article)
            return Response(serializer.data)
        # return Response{'TODO':'ДОБАВИТЬ УДАЛЕНИЕ КОМЕНТА'}


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyFilter



    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context

    def get_permissions(self):
        if self.request.method == 'POST': # если пользователь хочет сделать одно из эти действий то у него бкдет проверяться токен
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsAuthor] #обновлять и удалять может тольок автор 
        return super().get_permissions()


class CategoryCreateReadUpdateDelete(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        method = self.request.method
        if method in permissions.SAFE_METHODS:
            self.permission_classes = [permissions.AllowAny]
        elif method in ['POST','DELETE']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
class PromotionCountView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = PromotionCountSerializer






    

