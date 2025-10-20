from rest_framework import serializers

from anime.models import Anime
from anime.serializers.genre import GenreSerializer
from anime.serializers.studio import StudioSerializer
from media.serializers import ImageSerializer


class AnimeSerializer(serializers.ModelSerializer):
    season_label = serializers.CharField(source='get_season_display', read_only=True)

    class Meta:
        model = Anime
        fields = [
            'id', 'mal_id', 'title', 'url', 'aired_from', 'aired_till', 'season', 'season_label', 'synopsis', 'rating'
        ]
        extra_kwargs = {
            'mal_id': {'validators': []},
        }


class AnimeRetrieveSerializer(serializers.ModelSerializer):
    season_label = serializers.CharField(source='get_season_display', read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    studios = StudioSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    episode_count = serializers.SerializerMethodField()
    character_count = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = [
            'id', 'mal_id', 'title', 'url', 'aired_from', 'aired_till', 'season', 'season_label', 'synopsis', 'rating',
            'character_count', 'episode_count', 'genres', 'studios', 'images', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'mal_id': {'validators': []},
        }

    def get_episode_count(self, obj):
        return obj.episodes.all().count()

    def get_character_count(self, obj):
        return obj.characters.all().count()
