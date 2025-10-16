from django.db import models

from anime.models import Character
from media.models import Image


class VoiceActor(models.Model):
    character = models.ForeignKey(Character, on_delete=models.PROTECT, related_name='voice_actors')
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField()
    images = models.ManyToManyField(Image, related_name='voice_actors', blank=True)
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.name
