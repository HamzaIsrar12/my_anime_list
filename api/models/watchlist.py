from django.db import models

from api.models import Anime, User
from core.models import BaseModel


class WatchList(BaseModel):
    class ListType(models.TextChoices):
        WATCH_LATER = 'watch_later'
        WATCHING = 'watching'
        WATCHED = 'watched'

    user = models.ForeignKey(User, related_name='watchlist_entries', on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, related_name='watchlist_entries', on_delete=models.CASCADE)
    type = models.CharField(max_length=11, choices=ListType.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'anime'], name='unique_watchlist')
        ]
