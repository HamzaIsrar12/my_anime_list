from django.contrib.auth import get_user_model
from rest_framework import serializers

from anime.models import Anime, Character
from engagement.models import Review, CharacterLike

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    anime_id = serializers.PrimaryKeyRelatedField(queryset=Anime.objects.all(), source='anime')
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')

    class Meta:
        model = Review
        fields = ['id', 'anime_id', 'user_id', 'rating', 'message', 'created_at']


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['message', 'rating']


class CharacterLikeSerializer(serializers.ModelSerializer):
    class CharacterMiniSerializer(serializers.ModelSerializer):
        class Meta:
            model = Character
            fields = ['id', 'name']

    character = CharacterMiniSerializer(read_only=True)
    character_id = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all(), write_only=True)

    class Meta:
        model = CharacterLike
        fields = ['id', 'character_id', 'character', 'created_at']
