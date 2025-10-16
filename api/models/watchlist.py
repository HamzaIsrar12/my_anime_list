from django.db import models

from api.models import Anime, User
from core.models import BaseModel, IntegerChoicesExtended


class WatchList(BaseModel):
    class ListType(IntegerChoicesExtended):
        WATCH_LATER = 0, 'watch_later'
        WATCHING = 1, 'watching'
        WATCHED = 2, 'watched'

    user = models.ForeignKey(User, related_name='watchlist_entries', on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, related_name='watchlist_entries', on_delete=models.CASCADE)
    type = models.IntegerField(choices=ListType.choices, default=ListType.WATCH_LATER)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'anime'], name='unique_watchlist')
        ]
