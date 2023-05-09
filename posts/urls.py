from rest_framework.routers import DefaultRouter
from .views import PromotionViewSet,CommentViewSet,CompanyViewSet,CategoryViewSet,PromotionCountView

router = DefaultRouter()
router.register('promotion',PromotionViewSet, 'promotion'),
router.register('comment', CommentViewSet, 'comments'),
router.register('company', CompanyViewSet, 'company'),
router.register('category',CategoryViewSet,'category')
router.register('categories/<int:pk>/promotions_count/', PromotionCountView, 'category-promotions-count'),

urlpatterns = router.urls