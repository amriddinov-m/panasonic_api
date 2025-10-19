from rest_framework import serializers

from user.models import BalanceHistory, UserBalance


class UserBalanceSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()

    class Meta:
        model = UserBalance
        fields = '__all__'

    def get_user_fullname(self, obj):
        return obj.user.get_full_name()


class BalanceHistorySerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()

    class Meta:
        model = BalanceHistory
        fields = '__all__'

    def get_user_fullname(self, obj):
        return obj.balance.user.get_full_name()

    def create(self, validated_data):
        history_type = validated_data.get('history_type')
        amount = validated_data.get('amount')
        balance_obj = validated_data.get('balance')

        # Пополнение
        if history_type == BalanceHistory.HistoryType.income:
            balance_obj.balance_amount += amount

        # Расход / Вывод
        elif history_type in [BalanceHistory.HistoryType.outcome, BalanceHistory.HistoryType.withdraw]:
            if balance_obj.balance_amount < amount:
                raise serializers.ValidationError("Недостаточно средств на балансе.")
            balance_obj.balance_amount -= amount

        balance_obj.save()
        return super().create(validated_data)
