from django.contrib import admin

from api.models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass
