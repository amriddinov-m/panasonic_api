from rest_framework import serializers
from .models import (
    Status, UnitType, ProductCategory, Product,
    Warehouse, WarehouseProduct,
    Income, IncomeItem, Outcome, OutcomeItem
)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class WarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    client_fullname = serializers.SerializerMethodField()
    status_value = serializers.SerializerMethodField()
    class Meta:
        model = Income
        fields = '__all__'

    def get_user_fullname(self, obj):
        return obj.user.get_full_name()

    def get_client_fullname(self, obj):
        return obj.client.get_full_name()

    def get_status_value(self, obj):
        return obj.get_status_display()



class IncomeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeItem
        fields = '__all__'


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = '__all__'


class OutcomeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeItem
        fields = '__all__'
