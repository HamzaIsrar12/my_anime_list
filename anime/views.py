from django.db.models import Count
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from anime.models import Anime, Character
from anime.serializers import AnimeSerializer, CharacterSerializer, EpisodeSerializer
from anime.services import AnimeDataService
from engagement.serializers import ReviewSerializer


class AnimeSearchView(APIView, PageNumberPagination):
    def get(self, request):
        query = request.query_params.get('q')

        AnimeDataService.search_external_anime(query, timeout=4)
        anime = Anime.objects.filter(title__icontains=query).order_by('pk')

        page = self.paginate_queryset(anime, request)
        if page is not None:
            serializer = AnimeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AnimeSerializer(anime, many=True)
        return Response(serializer.data)


class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Anime.objects.order_by('pk')
    serializer_class = AnimeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genres__name']
    ordering_fields = ['title']
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=True, methods=['get'], url_path='episodes')
    def episodes(self, request, slug=None):
        episodes = self.get_object().episodes.order_by('pk')

        page = self.paginate_queryset(episodes)
        if page is not None:
            serializer = EpisodeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EpisodeSerializer(episodes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='characters')
    def characters(self, request, slug=None):
        characters = (
            Character.objects
            .filter(anime__slug=slug)
            .prefetch_related('voice_actors', 'images', 'liked_by')
            .order_by('pk')
        )

        page = self.paginate_queryset(characters)
        if page is not None:
            serializer = CharacterSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = CharacterSerializer(characters, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='reviews')
    def reviews(self, request, slug=None):
        reviews = self.get_object().reviews.order_by('-created_at')

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CharacterSerializer
    permission_classes = [AllowAny]
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'

    def get_queryset(self):
        return Character.objects.prefetch_related('images', 'liked_by', 'voice_actors').order_by('pk')

    @action(detail=False, methods=['get'], url_path='top')
    def top_characters(self, request):
        characters = self.get_queryset().annotate(total_likes=Count('liked_by', distinct=True)).order_by('-total_likes')

        page = self.paginate_queryset(characters)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(characters, many=True)
        return Response(serializer.data)
