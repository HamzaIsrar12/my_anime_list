from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.models import Anime, User
from core.models import BaseModel


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    message = models.TextField(blank=True)
