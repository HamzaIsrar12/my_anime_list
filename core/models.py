from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LabelLookupIntegerChoices(models.IntegerChoices):
    @classmethod
    def value_of(cls, label, default=None):
        label = str(label).lower()
        for (choice_value, choice_label) in cls.choices:
            if label == choice_label.lower():
                return choice_value

        return default
