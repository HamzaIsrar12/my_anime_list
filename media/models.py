from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from media.choices import ImageType


class Image(models.Model):
    type = models.PositiveSmallIntegerField(choices=ImageType.choices, default=ImageType.JPG)
    image_url = models.URLField(blank=True, null=True)
    small_image_url = models.URLField(blank=True, null=True)
    large_image_url = models.URLField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.image_url
