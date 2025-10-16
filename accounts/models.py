from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('anime.Anime', through='watchlist.WatchList', related_name='watchlist_by',
                                       blank=True)

    def __str__(self):
        return self.username
