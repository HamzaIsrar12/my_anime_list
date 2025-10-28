from django.urls import include, path
from rest_framework import routers

from anime.views import AnimeSearchView, AnimeViewSet, CharacterViewSet

router = routers.DefaultRouter()
router.register('anime', AnimeViewSet, basename='anime')
router.register('characters', CharacterViewSet, basename='characters')

urlpatterns = [
    path('anime/search/', AnimeSearchView.as_view(), name='anime-search'),
    path('', include(router.urls)),
]
