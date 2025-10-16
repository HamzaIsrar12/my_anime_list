from django.db import models


class Genre(models.Model):
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=20)
    url = models.URLField()

    def __str__(self):
        return self.name
