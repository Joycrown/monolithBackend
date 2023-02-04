from rest_framework import serializers
from portfolio.models import (
    FiatWallet,
    Cash,
    CreditCard,
    Transactions,
    Bank,
    Stock,
    StockWallet,
    StockTransaction,
    Crypto,
    CryptoWallet,
    CryptoTransaction,
    AccountStatement,
)


class CashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cash
        fields = ["currency_type", "amount"]


class FiatWalletSerializer(serializers.ModelSerializer):
    cash = CashSerializer(many=True)

    class Meta:
        model = FiatWallet
        fields = ["user", "cash"]


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = "__all__"


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class StockWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockWallet
        fields = "__all__"


class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = "__all__"


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = "__all__"


class CryptoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWallet
        fields = "__all__"


class CryptoTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoTransaction
        fields = "__all__"


class AccountStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatement
        fields = ('user', 'statement_start_date',
                  'statement_end_date', 'statement_type')


class FiatTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = "__all__"


# class TransactionsSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Transactions
#     fields = "__all__"


class OrderSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    qty = serializers.CharField(max_length=10)
    side = serializers.CharField(max_length=4)
    type = serializers.CharField(max_length=13)
    time_in_force = serializers.CharField(max_length=3)
    # body
    # "symbol": "ETHUSD",
    # "qty": "4.125",
    # "side": "buy",
    # "type": "market",
    # "time_in_force": "gtc"
