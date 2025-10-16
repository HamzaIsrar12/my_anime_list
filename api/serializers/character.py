from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Character, CharacterLike, VoiceActor
from api.serializers.common import ImageSerializer

User = get_user_model()


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
