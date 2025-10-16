from rest_framework import viewsets, mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.constants import PAGINATION_PAGE_SIZE
from engagement.models import Review, CharacterLike
from engagement.permissions import ReviewPermission
from engagement.serializers import ReviewSerializer, ReviewUpdateSerializer, CharacterLikeSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]
    pagination_class = PageNumberPagination
    pagination_class.page_size = PAGINATION_PAGE_SIZE

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer

        return super().get_serializer_class()


class CharacterLikeViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = CharacterLike.objects.select_related('character').order_by('pk')
    serializer_class = CharacterLikeSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = PAGINATION_PAGE_SIZE

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
