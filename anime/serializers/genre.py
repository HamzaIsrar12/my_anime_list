from rest_framework import serializers

from anime.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'mal_id', 'name', 'url']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }
