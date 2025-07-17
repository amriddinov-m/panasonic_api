from rest_framework import serializers
from .models import (
    Status, UnitType, ProductCategory, Product,
    Warehouse, WarehouseProduct,
    Income, IncomeItem, Outcome, OutcomeItem, Movement, MovementItem, Order, OrderItem
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
    product_name = serializers.SerializerMethodField()
    unit_type_name = serializers.SerializerMethodField()

    class Meta:
        model = WarehouseProduct
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name

    def get_unit_type_name(self, obj):
        return obj.unit_type.name


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
            warehouse_product, created = WarehouseProduct.objects.get_or_create(
                product=income_item.product,
                defaults={'count': income_item.count,
                          'unit_type': income_item.unit_type,
                          'price': income_item.price, }
            )
            if not created:
                warehouse_product.count += income_item.count
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

    def update(self, instance, validated_data):
        prev_status = instance.status
        new_status = validated_data.get('status', instance.status)

        instance = super().update(instance, validated_data)

        # логика вычитания товара при смене статуса на finished
        if prev_status != 'finished' and new_status == 'finished':
            for item in instance.items.all():
                try:
                    wp = WarehouseProduct.objects.get(product=item.product)
                    if wp.count >= item.count:
                        wp.count -= item.count
                        wp.save()
                    else:
                        raise serializers.ValidationError(
                            f"Недостаточно товара {item.product.name} на складе"
                        )
                except WarehouseProduct.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Товар {item.product.name} не найден на складе"
                    )

        return instance


class OutcomeItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OutcomeItem
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name


class MovementSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    warehouse_from_name = serializers.SerializerMethodField()
    warehouse_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Movement
        fields = '__all__'

    def get_user_fullname(self, obj):
        return obj.user.get_full_name()

    def get_warehouse_from_name(self, obj):
        return obj.warehouse_from.name

    def get_warehouse_to_name(self, obj):
        return obj.warehouse_to.name


class MovementItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = MovementItem
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name


class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_client_name(self, obj):
        return obj.client.get_full_name()

    def get_user_name(self, obj):
        return obj.user.get_full_name()


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    unit_type_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name

    def get_unit_type_name(self, obj):
        return obj.unit_type.name