from django.contrib.auth import get_user_model
from django.db import models

from anime.models.anime import Anime
from core.models import IntegerChoicesExtended
from media.models import Image

User = get_user_model()


class Character(models.Model):
    class Role(IntegerChoicesExtended):
        MAIN = 0, 'Main'
        SUPPORTING = 1, 'Supporting'

    anime = models.ForeignKey(Anime, related_name='characters', on_delete=models.CASCADE)
    mal_id = models.PositiveIntegerField(unique=True)
    images = models.ManyToManyField(Image, related_name='characters', blank=True)
    name = models.CharField(max_length=50)
    role = models.IntegerField(choices=Role.choices, default=Role.MAIN)
    liked_by = models.ManyToManyField(User, related_name='liked_characters', through='engagement.CharacterLike',
                                      blank=True)

    def __str__(self):
        return self.name
