from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.constants import PAGINATION_PAGE_SIZE
from api.models import Anime, Character
from api.serializers import AnimeRetrieveSerializer, AnimeSerializer, CharacterSerializer, EpisodeSerializer
from api.serializers.review import ReviewSerializer


class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Anime.objects.prefetch_related('genres').order_by('pk')
    serializer_class = AnimeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genres__name']
    ordering_fields = ['title']
    pagination_class = PageNumberPagination
    pagination_class.page_size = PAGINATION_PAGE_SIZE

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AnimeRetrieveSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'], url_path='episodes')
    def episodes(self, request, pk=None):
        episodes = self.get_object().episodes.order_by('pk')

        page = self.paginate_queryset(episodes)
        if page is not None:
            serializer = EpisodeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EpisodeSerializer(episodes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='characters')
    def characters(self, request, pk=None):
        characters = (
            Character.objects
            .filter(anime__id=pk)
            .prefetch_related('voice_actors', 'images', 'liked_by')
            .order_by('pk')
        )

        page = self.paginate_queryset(characters)
        if page is not None:
            serializer = CharacterSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='reviews')
    def reviews(self, request, pk=None):
        reviews = self.get_object().reviews.order_by('-created_at')

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
