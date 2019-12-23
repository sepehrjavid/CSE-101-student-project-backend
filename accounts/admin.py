from django.contrib import admin
from accounts.models import *

admin.site.register(BankAccount)
admin.site.register(AccountLog)
admin.site.register(AccountOwner)
