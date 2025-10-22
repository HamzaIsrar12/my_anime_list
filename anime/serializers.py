from rest_framework import serializers

from anime.models import Anime, Character, Episode, Genre, Studio, VoiceActor
from media.serializers import ImageSerializer


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


class AnimeSerializer(serializers.ModelSerializer):
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

    def get_fields(self):
        fields = super().get_fields()
        action = self.context.get('action', None)

        if action != 'retrieve':
            allowed_fields = [
                'id', 'mal_id', 'title', 'url', 'aired_from', 'aired_till', 'season', 'season_label', 'synopsis',
                'rating'
            ]
            fields = {key: value for (key, value) in fields.items() if key in allowed_fields}

        return fields

    def get_episode_count(self, obj):
        return obj.episodes.all().count()

    def get_character_count(self, obj):
        return obj.characters.all().count()


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'title_japanese', 'aired', 'filler', 'recap']


class VoiceActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceActor
        fields = ['id', 'name', 'language']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }


class CharacterSerializer(serializers.ModelSerializer):
    role_label = serializers.CharField(source='get_role_display', read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    voice_actors = VoiceActorSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'mal_id', 'name', 'images', 'role', 'role_label', 'likes', 'voice_actors']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }

    def get_likes(self, obj):
        return obj.liked_by.count()
