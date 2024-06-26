from rest_framework import serializers

from .models import BitcoinTransaction


class BitcoinTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitcoinTransaction
        fields = (
            "id",
            "user",
            "amount",
            "date",
            "description",
            "isFraud",
            "isConfirmed",
        )
        extra_kwargs = {"user": {"read_only": True}}
