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

    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', old_status)

        instance = super().update(instance, validated_data)

        if old_status != 'finished' and new_status == 'finished':
            self.create_or_update_product(instance)

        return instance

    def create_or_update_product(self, income):
        income_items = IncomeItem.objects.filter(income=income)
        for income_item in income_items:
            product = income_item.product
            count = income_item.count
            warehouse_product, created = WarehouseProduct.objects.get_or_create(
                product=product,
                defaults={'count': count}
            )
            if not created:
                warehouse_product.count += count
                warehouse_product.save()


class IncomeItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = IncomeItem
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name


class OutcomeSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    client_fullname = serializers.SerializerMethodField()
    status_value = serializers.SerializerMethodField()

    class Meta:
        model = Outcome
        fields = '__all__'

    def get_user_fullname(self, obj):
        return obj.user.get_full_name()

    def get_client_fullname(self, obj):
        return obj.client.get_full_name()

    def get_status_value(self, obj):
        return obj.get_status_display()


class OutcomeItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OutcomeItem
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name
