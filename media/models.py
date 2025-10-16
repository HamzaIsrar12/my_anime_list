from django.db import models

from core.models import IntegerChoicesExtended


class Image(models.Model):
    class Type(IntegerChoicesExtended):
        JPG = 0, 'jpg'
        WEBP = 1, 'webp'

    type = models.IntegerField(choices=Type.choices, default=Type.JPG)
    image_url = models.URLField(blank=True, null=True)
    small_image_url = models.URLField(blank=True, null=True)
    large_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.image_url
