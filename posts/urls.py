from rest_framework.routers import DefaultRouter
from .views import PromotionViewSet,CommentViewSet,CompanyViewSet,CategoryCreateReadUpdateDelete,PromotionCountView

router = DefaultRouter()
router.register('promotion',PromotionViewSet, 'promotion'),
router.register('comment', CommentViewSet, 'comments'),
router.register('company', CompanyViewSet, 'company'),
router.register('category',CategoryCreateReadUpdateDelete,'category')
router.register('categories/<int:pk>/promotions_count/', PromotionCountView, 'category-promotions-count'),

urlpatterns = router.urls