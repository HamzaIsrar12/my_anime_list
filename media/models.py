from django.db import models

from media.choices import ImageType


class Image(models.Model):
    type = models.IntegerField(choices=ImageType.choices, default=ImageType.JPG)
    image_url = models.URLField(blank=True, null=True)
    small_image_url = models.URLField(blank=True, null=True)
    large_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.image_url
