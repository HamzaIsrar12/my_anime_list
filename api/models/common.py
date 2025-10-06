from django.db import models


class Image(models.Model):
    class Type(models.TextChoices):
        JPG = 'jpg'
        WEBP = 'webp'

    type = models.CharField(max_length=4, choices=Type.choices, default=Type.JPG)
    image_url = models.URLField(blank=True, null=True)
    small_image_url = models.URLField(blank=True, null=True)
    large_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.image_url
