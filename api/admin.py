from django.contrib import admin

from api.models import Status, Income, Outcome, Product, UnitType, ProductCategory


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    pass
