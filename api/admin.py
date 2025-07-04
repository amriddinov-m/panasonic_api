from django.contrib import admin

from api.models import Status, Income, Outcome


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    pass
