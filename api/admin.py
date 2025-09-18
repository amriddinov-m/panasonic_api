from django.contrib import admin

from api.models import Status, Income, Outcome, Product, UnitType, ProductCategory, IncomeItem, WarehouseProduct, \
    Movement, MovementItem, Warehouse, Report, ReportItem, Order, OrderItem


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

class ReportItemInline(admin.TabularInline):
    model = ReportItem
    extra = 0



@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportItemInline]


@admin.register(ReportItem)
class ReportItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'id', 'client', 'user', 'total_amount', 'status'
    list_filter = 'client',


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass
