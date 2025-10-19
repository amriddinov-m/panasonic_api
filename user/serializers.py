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
