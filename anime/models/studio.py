from django.db import models


class Studio(models.Model):
    mal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name
