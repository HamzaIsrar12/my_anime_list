from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Image

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['type', 'image_url', 'small_image_url', 'large_image_url']
