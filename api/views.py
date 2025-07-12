from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .filters import WarehouseProductFilter
from .serializers import *


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.order_by('-id')
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'status', '_type', 'created', 'user']


class UnitTypeViewSet(viewsets.ModelViewSet):
    queryset = UnitType.objects.order_by('-id')
    serializer_class = UnitTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'status', 'created', 'user']


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.order_by('-id')
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'status', 'created', 'user']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'unit_type', 'status', 'created', 'user']


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.order_by('-id')
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'created', 'user']


class WarehouseProductViewSet(viewsets.ModelViewSet):
    queryset = WarehouseProduct.objects.order_by('-id')
    serializer_class = WarehouseProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseProductFilter


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.order_by('-id')
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'created', 'user', 'status']


class IncomeItemViewSet(viewsets.ModelViewSet):
    queryset = IncomeItem.objects.order_by('-id')
    serializer_class = IncomeItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['income', 'product', 'unit_type', 'status', 'user']


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.order_by('-id')
    serializer_class = OutcomeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'created', 'user', 'status']


class OutcomeItemViewSet(viewsets.ModelViewSet):
    queryset = OutcomeItem.objects.order_by('-id')
    serializer_class = OutcomeItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['outcome', 'product', 'unit_type', 'status', 'user']
