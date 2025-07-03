from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import *


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class UnitTypeViewSet(viewsets.ModelViewSet):
    queryset = UnitType.objects.all()
    serializer_class = UnitTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class WarehouseProductViewSet(viewsets.ModelViewSet):
    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class IncomeItemViewSet(viewsets.ModelViewSet):
    queryset = IncomeItem.objects.all()
    serializer_class = IncomeItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class OutcomeItemViewSet(viewsets.ModelViewSet):
    queryset = OutcomeItem.objects.all()
    serializer_class = OutcomeItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
