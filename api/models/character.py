from django.db import models

from api.models import User
from api.models.anime import Anime
from api.models.common import Image
from core.models import BaseModel


class Character(models.Model):
    class Role(models.TextChoices):
        MAIN = 'Main'
        SUPPORTING = 'Supporting'

    anime = models.ForeignKey(Anime, related_name='characters', on_delete=models.CASCADE)
    mal_id = models.PositiveIntegerField(unique=True)
    images = models.ManyToManyField(Image, related_name='characters', blank=True)
    name = models.CharField(max_length=50)
    role = models.CharField(choices=Role.choices, max_length=10, default=Role.MAIN)
    liked_by = models.ManyToManyField(User, related_name='liked_characters', through='CharacterLike', blank=True)

    def __str__(self):
        return self.name


class VoiceActor(models.Model):
    character = models.ForeignKey(Character, on_delete=models.PROTECT, related_name='voice_actors')
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField()
    images = models.ManyToManyField(Image, related_name='voice_actors', blank=True)
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CharacterLike(BaseModel):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['character', 'user'], name='unique_character')
        ]
