from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import BankAccount
from transaction.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    fromAccountNumber = serializers.SerializerMethodField()
    toAccountNumber = serializers.SerializerMethodField()
    fromAccount = serializers.CharField(max_length=18, write_only=True, required=False)
    toAccount = serializers.CharField(max_length=18, write_only=True, required=False)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "fromAccount",
            "fromAccountNumber",
            "toAccount",
            "toAccountNumber",
            "amount",
            "definition",
            "cash"
        ]

        read_only_fields = ("id", "fromAccountNumber", "toAccountNumber")

    def get_toAccountNumber(self, obj):
        if obj.toAccount is not None:
            return obj.toAccount.accountNumber
        return None

    def get_fromAccountNumber(self, obj):
        if obj.fromAccount is not None:
            return obj.fromAccount.accountNumber
        return None

    def validate(self, attrs):
        if attrs.get("cash"):
            myFields = ["toAccount", "fromAccount"]
            if len([attrs.get(x) for x in myFields if attrs.get(x) is None]) != 1:
                raise ValidationError("Invalid value for cash")
        else:
            if attrs.get("fromAccount") is None or attrs.get("toAccount") is None:
                raise ValidationError("Invalid value for cash")
        fromAccount = attrs.get("fromAccount")
        toAccount = attrs.get("toAccount")
        if fromAccount is not None and fromAccount.credit - attrs.get("amount") < 0:
            raise ValidationError("not enough credit")
        if fromAccount is not None and toAccount is not None and fromAccount.accountNumber == toAccount.accountNumber:
            raise ValidationError("account numbers are the same")
        return attrs

    def validate_fromAccount(self, attr):
        qs = BankAccount.objects.filter(accountNumber=attr)
        if not qs.exists():
            raise ValidationError("from account is not valid")
        return qs.first()

    def validate_toAccount(self, attr):
        qs = BankAccount.objects.filter(accountNumber=attr)
        if not qs.exists():
            raise ValidationError("to account is not valid")
        return qs.first()
