import django_filters
from .models import WarehouseProduct

class WarehouseProductFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(
        field_name='product__name',
        lookup_expr='icontains',
        label='Название продукта (по части слова)'
    )

    class Meta:
        model = WarehouseProduct
        fields = ['product', 'product_name', 'warehouse', 'status', 'created', 'user', 'product__category']
