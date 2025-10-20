import django_filters
from .models import WarehouseProduct, Outcome, Order, Income


class WarehouseProductFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(
        field_name='product__name',
        lookup_expr='icontains',
        label='Название продукта (по части слова)'
    )

    class Meta:
        model = WarehouseProduct
        fields = ['product', 'product_name', 'warehouse', 'status', 'created', 'user', 'product__category']


class IncomeFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name='created', lookup_expr='gte', label='Дата с'
    )
    to_date = django_filters.DateFilter(
        field_name='created', lookup_expr='lte', label='Дата по'
    )

    class Meta:
        model = Income
        fields = ['client', 'created', 'user', 'status', 'warehouse', 'from_date', 'to_date']


class OutcomeFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name='created', lookup_expr='gte', label='Дата с'
    )
    to_date = django_filters.DateFilter(
        field_name='created', lookup_expr='lte', label='Дата по'
    )

    class Meta:
        model = Outcome
        fields = ['client', 'user', 'status', 'warehouse', 'reason', 'from_date', 'to_date']


class OrderFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(
        field_name='created', lookup_expr='gte', label='Дата с'
    )
    to_date = django_filters.DateFilter(
        field_name='created', lookup_expr='lte', label='Дата по'
    )

    class Meta:
        model = Order
        fields = ['client', 'user', 'status', 'created', 'from_date', 'to_date']
