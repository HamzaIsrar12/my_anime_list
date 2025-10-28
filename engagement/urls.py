from rest_framework import routers

from engagement.views import CharacterLikeViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register('likes', CharacterLikeViewSet, basename='likes')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = router.urls
