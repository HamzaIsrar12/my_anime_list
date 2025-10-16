from rest_framework import routers

from anime.views import AnimeViewSet, CharacterViewSet

router = routers.DefaultRouter()
router.register('anime', AnimeViewSet, basename='anime')
router.register('characters', CharacterViewSet, basename='characters')

urlpatterns = router.urls
