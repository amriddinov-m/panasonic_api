from django.contrib import admin

from api.models import Status, Income


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass
