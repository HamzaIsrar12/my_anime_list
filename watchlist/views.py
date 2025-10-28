from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from watchlist.models import WatchList
from watchlist.serializers import WatchListSerializer


class WatchListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['type']
    search_fields = ['anime__title']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user).select_related('anime').order_by('anime__title')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        watchlist, _ = WatchList.objects.update_or_create(
            anime=data['anime'],
            user=self.request.user,
            defaults={
                'type': data['type'],
            }
        )
        return Response(self.get_serializer(watchlist).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
