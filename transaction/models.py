from django.db import models


class Transaction(models.Model):
    fromAccount = models.ForeignKey('accounts.BankAccount', on_delete=models.CASCADE, null=True,
                                    related_name="transactionsFrom")
    toAccount = models.ForeignKey('accounts.BankAccount', on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    definition = models.TextField(blank=True)
    cash = models.BooleanField(default=False)
