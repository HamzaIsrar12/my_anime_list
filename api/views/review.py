from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api.constants import PAGINATION_PAGE_SIZE
from api.models import Review
from api.permissions.review import ReviewPermission
from api.serializers.review import ReviewSerializer, ReviewUpdateSerializer


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
