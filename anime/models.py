from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from anime.choices import Role, Season
from core.models import BaseModel
from media.models import Image

User = get_user_model()


class Genre(models.Model):
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=20)
    url = models.URLField()

    def __str__(self):
        return self.name


class Studio(models.Model):
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name


class Anime(BaseModel):
    mal_id = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=100)
    url = models.URLField()
    aired_from = models.DateField(blank=True, null=True)
    aired_till = models.DateField(blank=True, null=True)
    synopsis = models.TextField()
    season = models.PositiveSmallIntegerField(choices=Season.choices, blank=True, null=True)
    images = GenericRelation(Image, related_query_name='anime', blank=True)
    studios = models.ManyToManyField('Studio', related_name='anime')
    genres = models.ManyToManyField('Genre', related_name='anime')
    rating = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=100)
    title_japanese = models.CharField(max_length=100, blank=True, null=True)
    aired = models.DateField(blank=True, null=True)
    filler = models.BooleanField(default=False)
    recap = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Character(models.Model):
    anime = models.ForeignKey(Anime, related_name='characters', on_delete=models.CASCADE)
    mal_id = models.PositiveIntegerField(unique=True)
    images = GenericRelation(Image, related_query_name='character', blank=True)
    name = models.CharField(max_length=50)
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.MAIN)
    liked_by = models.ManyToManyField(
        User, related_name='liked_characters', through='engagement.CharacterLike', blank=True
    )

    def __str__(self):
        return self.name


class VoiceActor(models.Model):
    character = models.ForeignKey(Character, on_delete=models.PROTECT, related_name='voice_actors')
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField()
    images = GenericRelation(Image, related_query_name='voice_actor', blank=True)
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.name
