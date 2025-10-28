from core.models import LabelLookupIntegerChoices


class Season(LabelLookupIntegerChoices):
    SPRING = 0, 'Spring'
    SUMMER = 1, 'Summer'
    FALL = 2, 'Fall'
    WINTER = 3, 'Winter'


class Role(LabelLookupIntegerChoices):
    MAIN = 0, 'Main'
    SUPPORTING = 1, 'Supporting'
