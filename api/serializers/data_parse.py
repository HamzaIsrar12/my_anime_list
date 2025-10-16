from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_datetime
from rest_framework import serializers

from api.models import Anime, Character, Episode, Genre, Image, Studio, VoiceActor
from api.serializers.anime import GenreSerializer, StudioSerializer

User = get_user_model()


class ImageExternalCreateSerializer(serializers.ModelSerializer):
    images_data = serializers.DictField(
        write_only=True,
        child=serializers.DictField(),
        required=False
    )

    class Meta:
        model = Image
        fields = ['type', 'image_url', 'small_image_url', 'large_image_url', 'images_data']

    @transaction.atomic
    def create(self, validated_data):
        related_model = self.context.get('related_model')
        images_data = validated_data.get('images_data')

        for image_type, urls in images_data.items():
            image, _ = Image.objects.update_or_create(
                type=Image.Type.value_of(image_type),
                image_url=urls.get('image_url', None),
                defaults={
                    'image_url': urls.get('image_url', None),
                    'small_image_url': urls.get('small_image_url', None),
                    'large_image_url': urls.get('large_image_url', None),
                }
            )
            related_model.images.add(image)

        return related_model


class AnimeExternalCreateSerializer(serializers.ModelSerializer):
    images = serializers.DictField(
        child=serializers.DictField(),
        write_only=True,
        allow_empty=True,
        required=False
    )
    aired = serializers.DictField(write_only=True, allow_empty=True, required=False)
    studios = StudioSerializer(many=True, write_only=True, allow_empty=True, required=False)
    genres = GenreSerializer(many=True, write_only=True, allow_empty=True, required=False)
    season = serializers.CharField(required=False)

    class Meta:
        model = Anime
        fields = ['mal_id', 'url', 'title', 'aired_from', 'aired_till', 'rating', 'synopsis', 'season', 'images',
                  'studios', 'genres', 'aired']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }

    @transaction.atomic
    def create(self, validated_data):
        mal_id = validated_data.get('mal_id')
        studios_data = validated_data.pop('studios', [])
        genres_data = validated_data.pop('genres', [])
        images_data = validated_data.pop('images', {})
        aired_data = validated_data.pop('aired', {})
        season_data = validated_data.pop('season')

        validated_data['season'] = Anime.Season.value_of(season_data)

        defaults = {k: v for k, v in validated_data.items()}

        anime, _ = Anime.objects.update_or_create(defaults=defaults, mal_id=mal_id)

        for genre_data in genres_data:
            genre, _ = Genre.objects.get_or_create(**genre_data)
            anime.genres.add(genre)

        for studio_data in studios_data:
            studio, _ = Studio.objects.get_or_create(**studio_data)
            anime.studios.add(studio)

        image_serializer = ImageExternalCreateSerializer(
            data={'images_data': images_data},
            context={'related_model': anime}
        )
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save()

        aired_from = aired_data.pop('from', '')
        aired_till = aired_data.pop('to', '')

        if aired_from:
            anime.aired_from = parse_datetime(aired_from)
        if aired_till:
            anime.aired_till = parse_datetime(aired_till)

        anime.save()

        return anime


class CharacterExternalCreateSerializer(serializers.ModelSerializer):
    images = serializers.DictField(
        child=serializers.DictField(),
        write_only=True,
        allow_empty=True,
        required=False,
    )
    voice_actors = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        allow_empty=True
    )
    role = serializers.CharField()

    class Meta:
        model = Character
        fields = ['mal_id', 'name', 'role', 'images', 'voice_actors']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }

    def to_internal_value(self, data):
        character = data.get('character') or {}
        flat = {
            'mal_id': character.get('mal_id'),
            'name': character.get('name'),
            'images': character.get('images') or {},
            'role': data.get('role') or Character.Role.MAIN,
            'voice_actors': data.get('voice_actors') or [],
        }
        return super().to_internal_value(flat)

    @transaction.atomic
    def create(self, validated_data):
        anime = self.context.get('anime')

        mal_id = validated_data.get('mal_id')
        name = validated_data.get('name')
        role = validated_data.get('role')
        images_data = validated_data.get('images', {})
        voice_actors_data = validated_data.get('voice_actors', [])

        character, _ = Character.objects.update_or_create(
            mal_id=mal_id,
            defaults={
                'name': name,
                'role': Character.Role.value_of(role, Character.Role.MAIN.value),
                'anime': anime,
            }
        )

        image_serializer = ImageExternalCreateSerializer(
            data={'images_data': images_data},
            context={'related_model': character}
        )
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save()

        vs = VoiceActorExternalCreateSerializer(data=voice_actors_data, many=True, context={'character': character})
        vs.is_valid()
        vs.save()

        return character


class VoiceActorExternalCreateSerializer(serializers.ModelSerializer):
    voice_actors = serializers.DictField(write_only=True)

    class Meta:
        model = VoiceActor
        fields = ['mal_id', 'url', 'name', 'language', 'voice_actors']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }

    def to_internal_value(self, data):
        person = data.get('person')
        flat = {
            'mal_id': person.get('mal_id'),
            'name': person.get('name'),
            'images': person.get('images') or {},
            'url': person.get('url'),
            'language': data.get('language'),
        }
        return super().to_internal_value(flat)

    def create(self, validated_data):
        character = self.context.get('character')
        images_data = validated_data.pop('images', {})

        voice_actor, _ = VoiceActor.objects.update_or_create(
            mal_id=validated_data.get('mal_id'),
            defaults={
                'name': validated_data.get('name'),
                'url': validated_data.get('url'),
                'language': validated_data.get('language'),
                'character': character,
            }
        )

        image_serializer = ImageExternalCreateSerializer(
            data={'images_data': images_data},
            context={'related_model': voice_actor}
        )
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save()

        return voice_actor


class EpisodeExternalCreateSerializer(serializers.ModelSerializer):
    aired = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=[
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%SZ',
        ],
    )

    class Meta:
        model = Episode
        fields = ['title', 'title_japanese', 'filler', 'recap', 'aired']

    def create(self, validated_data):
        anime = self.context.get('anime')

        episode, _ = Episode.objects.update_or_create(
            title=validated_data.get('title'),
            defaults={
                'title': validated_data.get('title', ''),
                'title_japanese': validated_data.get('title_japanese', None),
                'filler': validated_data.get('filler', False),
                'recap': validated_data.get('recap', False),
                'aired': validated_data.get('aired', None),
                'anime': anime,
            }
        )

        return episode
