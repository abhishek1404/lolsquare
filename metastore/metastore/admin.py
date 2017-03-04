import logging

from django.contrib import admin



from .models import (Videos)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    save_as = True

