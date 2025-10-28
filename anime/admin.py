from django.contrib import admin

from anime.models import Anime, Character, Episode, Genre, Studio, VoiceActor

admin.site.register(Anime)
admin.site.register(Character)
admin.site.register(Episode)
admin.site.register(Genre)
admin.site.register(Studio)
admin.site.register(VoiceActor)
