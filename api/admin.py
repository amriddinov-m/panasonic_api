from django.contrib import admin

from api.models import Status, Income, Outcome, Product, UnitType, ProductCategory, IncomeItem, WarehouseProduct, \
    Movement, MovementItem, Warehouse


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(WarehouseProduct)
class WarehouseProductAdmin(admin.ModelAdmin):
    pass

class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name',)
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


@admin.register(UnitType)
class UnitTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(IncomeItem)
class IncomeItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    pass


@admin.register(MovementItem)
class MovementItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    pass