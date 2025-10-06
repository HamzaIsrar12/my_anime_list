from django.db.models import Count
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import Character, CharacterLike
from api.serializers import CharacterLikeSerializer, CharacterSerializer


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.prefetch_related('images', 'liked_by', 'voice_actors').order_by('pk')
    serializer_class = CharacterSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20
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


class CharacterLikeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = CharacterLike.objects.select_related('character').order_by('pk')
    serializer_class = CharacterLikeSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        like, _ = CharacterLike.objects.update_or_create(
            character=data['character_id'],
            user=self.request.user
        )
        return Response(self.get_serializer(like).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
