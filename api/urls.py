from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (AnimeViewSet, CharacterLikeViewSet, CharacterViewSet,
                       RegisterAPIView, ReviewViewSet, WatchListViewSet)

router = routers.DefaultRouter()
router.register('anime', AnimeViewSet)
router.register('watchlist', WatchListViewSet)
router.register('characters', CharacterViewSet)
router.register('likes', CharacterLikeViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
