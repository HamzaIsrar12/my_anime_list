from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseModel

User = get_user_model()


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    message = models.TextField(blank=True)


class CharacterLike(BaseModel):
    character = models.ForeignKey('anime.Character', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['character', 'user'], name='unique_character')
        ]
