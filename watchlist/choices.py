from core.models import LabelLookupIntegerChoices


class ListType(LabelLookupIntegerChoices):
    WATCH_LATER = 0, 'Watch Later'
    WATCHING = 1, 'Watching'
    WATCHED = 2, 'Watched'
