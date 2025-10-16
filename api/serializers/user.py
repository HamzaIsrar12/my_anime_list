from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Anime, WatchList

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class WatchListSerializer(serializers.ModelSerializer):
    anime_id = serializers.PrimaryKeyRelatedField(source='anime', queryset=Anime.objects.all(), write_only=True)
    anime_title = serializers.StringRelatedField(source='anime.title', read_only=True)
    type_label = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = WatchList
        fields = ['id', 'type', 'type_label', 'anime_id', 'anime_title', 'created_at']


class WatchListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ['type']
