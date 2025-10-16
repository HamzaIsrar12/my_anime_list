from django.db import models

from core.models import BaseModel, IntegerChoicesExtended
from media.models import Image


class Anime(BaseModel):
    class Season(IntegerChoicesExtended):
        SPRING = 0, 'Spring'
        SUMMER = 1, 'Summer'
        FALL = 2, 'Fall'
        WINTER = 3, 'Winter'

    mal_id = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=100)
    url = models.URLField()
    aired_from = models.DateField(blank=True, null=True)
    aired_till = models.DateField(blank=True, null=True)
    synopsis = models.TextField()
    season = models.IntegerField(choices=Season.choices, blank=True, null=True)
    images = models.ManyToManyField(Image, related_name='anime', blank=True)
    studios = models.ManyToManyField('Studio', related_name='anime')
    genres = models.ManyToManyField('Genre', related_name='anime')
    rating = models.CharField(max_length=100)

    def __str__(self):
        return self.title
