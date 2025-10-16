from django.db import models

from anime.models import Anime


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=100)
    title_japanese = models.CharField(max_length=100, blank=True, null=True)
    aired = models.DateField(blank=True, null=True)
    filler = models.BooleanField(default=False)
    recap = models.BooleanField(default=False)

    def __str__(self):
        return self.title
