from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromotionViewSet, CommentViewSet, CompanyViewSet, CategoryViewSet, PostPromotionLike

router = DefaultRouter()
router.register('promotion', PromotionViewSet, basename='promotion')
router.register('comment', CommentViewSet, basename='comment')
router.register('company', CompanyViewSet, basename='company')
router.register('category', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
    path('promotion/<int:promotion_id>/like/', PostPromotionLike.as_view()),
]





