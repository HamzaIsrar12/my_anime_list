from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.models import Anime, Episode, Genre, Studio
from api.serializers.common import ImageSerializer

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'mal_id', 'name', 'url']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'mal_id', 'name', 'url']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'title_japanese', 'aired', 'filler', 'recap']


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['id', 'mal_id', 'title', 'url', 'aired_from', 'aired_till', 'season', 'synopsis', 'rating']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }


class AnimeRetrieveSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    studios = StudioSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    episode_count = serializers.SerializerMethodField()
    character_count = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = ['id', 'mal_id', 'title', 'url', 'aired_from', 'aired_till', 'season', 'synopsis', 'rating',
                  'character_count', 'episode_count', 'genres', 'studios', 'images']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }

    def get_episode_count(self, obj) -> int:
        return obj.episodes.all().count()

    def get_character_count(self, obj) -> int:
        return obj.characters.all().count()
