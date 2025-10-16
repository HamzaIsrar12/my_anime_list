from rest_framework import serializers

from anime.models import Episode


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'title_japanese', 'aired', 'filler', 'recap']
