from rest_framework import serializers

from anime.models import Studio


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'mal_id', 'name', 'url']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }
