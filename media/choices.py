from core.models import LabelLookupIntegerChoices


class ImageType(LabelLookupIntegerChoices):
    JPG = 0, 'jpg'
    WEBP = 1, 'webp'
