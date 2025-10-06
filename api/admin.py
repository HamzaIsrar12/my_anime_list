from django.contrib import admin

from api import models

admin.site.register(models.Image)
admin.site.register(models.Studio)
admin.site.register(models.Genre)
admin.site.register(models.Character)
admin.site.register(models.VoiceActor)
admin.site.register(models.Anime)
admin.site.register(models.Episode)
admin.site.register(models.WatchList)
admin.site.register(models.User)
admin.site.register(models.CharacterLike)
