from rest_framework import routers

from watchlist.views import WatchListViewSet

router = routers.DefaultRouter()
router.register('watchlist', WatchListViewSet, basename='watchlist')

urlpatterns = router.urls
