from rest_framework import serializers

from anime.models import Character
from anime.serializers import VoiceActorSerializer
from media.serializers import ImageSerializer


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
