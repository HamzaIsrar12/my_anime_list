from django.contrib.auth import get_user_model
from rest_framework import serializers

from anime.models import Anime, Character
from engagement.models import CharacterLike, Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    anime_id = serializers.PrimaryKeyRelatedField(queryset=Anime.objects.all(), source='anime')
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='reviews-detail')

    class Meta:
        model = Review
        fields = ['id', 'anime_id', 'user_id', 'rating', 'message', 'url', 'created_at']

    def get_fields(self):
        fields = super().get_fields()
        action = self.context.get('action', None)

        if action in ['update', 'partial_update']:
            allowed_fields = ['message', 'rating']
            fields = {key: value for key, value in fields.items() if key in allowed_fields}

        return fields


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
