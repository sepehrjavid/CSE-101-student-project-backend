import time

from django.db import models


class AccountOwner(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=11)
    nationalCode = models.CharField(max_length=10, unique=True)


class BankAccount(models.Model):
    ACCOUNT_STATE = (
        ("O", "Open"),
        ("B", "Blocked"),
        ("C", "Closed"),
    )
    accountNumber = models.CharField(max_length=18, unique=True)
    accountOwner = models.ForeignKey(AccountOwner, on_delete=models.CASCADE, related_name="accounts")
    credit = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=ACCOUNT_STATE, default="O")

    @staticmethod
    def createAccountNumber():
        id = str(time.time()).replace('.', '')
        if len(id) == 18:
            return id
        return id + (18 - len(id)) * "0"

    def createLog(self, amount, definition, logType):
        if logType == "+":
            self.credit += amount
        elif logType == "-":
            self.credit -= amount
        self.save()
        AccountLog.objects.create(account=self, amount=amount, definition=definition, logType=logType)


class AccountLog(models.Model):
    TYPES = (
        ("+", "+"),
        ("-", "-")
    )

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="logs")
    amount = models.IntegerField()
    definition = models.TextField(blank=True)
    logType = models.CharField(max_length=1, choices=TYPES)
    date = models.DateTimeField(auto_now_add=True)
