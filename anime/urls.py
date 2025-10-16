from django.urls import include, path
from rest_framework import routers

from anime.views import AnimeViewSet, CharacterViewSet

router = routers.DefaultRouter()
router.register('anime', AnimeViewSet)
router.register('characters', CharacterViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
