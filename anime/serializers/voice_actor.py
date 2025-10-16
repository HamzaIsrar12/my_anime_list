from rest_framework import serializers

from anime.models import VoiceActor


class VoiceActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceActor
        fields = ['id', 'name', 'language']
        extra_kwargs = {
            'mal_id': {'validators': []},
        }
