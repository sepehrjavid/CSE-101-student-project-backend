from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import BankAccount, AccountOwner, AccountLog


class AccountOwnerSerializer(serializers.ModelSerializer):
    accounts = serializers.SerializerMethodField()

    class Meta:
        model = AccountOwner
        fields = [
            "firstName",
            "lastName",
            "phoneNumber",
            "nationalCode",
            "accounts"
        ]

        read_only_fields = ("accounts",)

    def get_accounts(self, obj):
        return [{"accountNumber": x.accountNumber, "status": x.status} for x in obj.accounts.all()]


class BankAccountSerializer(serializers.ModelSerializer):
    accountOwner = AccountOwnerSerializer()

    class Meta:
        model = BankAccount
        fields = [
            "accountNumber",
            "accountOwner",
            "credit",
            "status"
        ]

        read_only_fields = ("accountNumber", "credit", "status")

    def create(self, validated_data):
        accountOwnerData = validated_data.pop("accountOwner")
        accountOwner = AccountOwner.objects.create(**accountOwnerData)

        return BankAccount.objects.create(accountOwner=accountOwner, accountNumber=BankAccount.createAccountNumber())


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password"
        ]

        read_only_fields = ("password",)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data.pop("username"))
        user.set_password(validated_data.pop("password"))
        user.save()
        return user


class AccountLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountLog
        fields = [
            "id",
            "amount",
            "definition",
            "logType",
            "date"
        ]


class BankAccountNumberSerializer(serializers.Serializer):
    accountNumber = serializers.CharField(max_length=18)


class AddAccountToAccountOwnerSerializer(serializers.Serializer):
    nationalCode = serializers.CharField(max_length=10)
