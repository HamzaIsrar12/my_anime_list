from rest_framework import serializers

from api.models import Anime, Review, User


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
