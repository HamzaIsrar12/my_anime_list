from django.db.models import Count
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from anime.models import Anime, Character
from anime.serializers import AnimeRetrieveSerializer, AnimeSerializer, CharacterSerializer, EpisodeSerializer
from engagement.serializers import ReviewSerializer


class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Anime.objects.prefetch_related('genres').order_by('pk')
    serializer_class = AnimeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genres__name']
    ordering_fields = ['title']

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


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.prefetch_related('images', 'liked_by', 'voice_actors').order_by('pk')
    serializer_class = CharacterSerializer
    permission_classes = [AllowAny]
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]

    @action(detail=False, methods=['get'], url_path='top')
    def top_characters(self, request):
        characters = self.get_queryset().annotate(total_likes=Count('liked_by', distinct=True)).order_by('-total_likes')

        page = self.paginate_queryset(characters)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(characters, many=True)
        return Response(serializer.data)
