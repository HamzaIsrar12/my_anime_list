from django.contrib.auth import get_user_model
from rest_framework import serializers

from media.models import Image

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    type_label = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Image
        fields = ['type', 'type_label', 'image_url', 'small_image_url', 'large_image_url']
