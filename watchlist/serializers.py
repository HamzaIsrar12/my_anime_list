from django.contrib.auth import get_user_model
from rest_framework import serializers

from anime.models import Anime
from watchlist.models import WatchList

User = get_user_model()


class WatchListSerializer(serializers.ModelSerializer):
    anime_id = serializers.PrimaryKeyRelatedField(source='anime', queryset=Anime.objects.all(), write_only=True)
    anime_title = serializers.StringRelatedField(source='anime.title', read_only=True)
    type_label = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = WatchList
        fields = ['id', 'type', 'type_label', 'anime_id', 'anime_title', 'created_at']

    def get_fields(self):
        fields = super().get_fields()
        action = self.context.get('action', None)

        if action in ['update', 'partial_update']:
            allowed_fields = ['type', 'type_label', 'anime_title']
            fields = {key: value for key, value in fields.items() if key in allowed_fields}

        return fields
