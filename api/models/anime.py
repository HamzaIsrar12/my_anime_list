from django.db import models

from api.models.common import Image
from core.models import BaseModel


class Anime(BaseModel):
    class Season(models.TextChoices):
        SPRING = 'spring'
        SUMMER = 'summer'
        FALL = 'fall'
        WINTER = 'winter'

    mal_id = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=100)
    url = models.URLField()
    aired_from = models.DateField(blank=True, null=True)
    aired_till = models.DateField(blank=True, null=True)
    synopsis = models.TextField()
    season = models.CharField(max_length=7, choices=Season.choices, blank=True, null=True)
    images = models.ManyToManyField(Image, related_name='anime', blank=True)
    studios = models.ManyToManyField('Studio', related_name='anime')
    genres = models.ManyToManyField('Genre', related_name='anime')
    rating = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Studio(models.Model):
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=20)
    url = models.URLField()

    def __str__(self):
        return self.name


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=100)
    title_japanese = models.CharField(max_length=100, blank=True, null=True)
    aired = models.DateField(blank=True, null=True)
    filler = models.BooleanField(default=False)
    recap = models.BooleanField(default=False)

    def __str__(self):
        return self.title
