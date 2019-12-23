from django.urls import path, re_path

from accounts.views import BankAccountListCreateView, SignUpView, BankAccountRetrieveView, GetBankAccountLogsView, \
    AddAccountToAccountOwnerView, GetAccountOwnerDataView, CloseAccountView, BlockAccountView

app_name = "accounts"

urlpatterns = [
    path("BankAccountListCreate", BankAccountListCreateView.as_view()),
    path("User/SignUp", SignUpView.as_view()),
    path("GetBankAccountLogs", GetBankAccountLogsView.as_view()),
    path("AddAccountToAccountOwner", AddAccountToAccountOwnerView.as_view()),
    path("CloseAccount", CloseAccountView.as_view()),
    path("BlockAccount", BlockAccountView.as_view()),
    re_path(r"^BankAccountRetrieve/(?P<accountNumber>\d+)$", BankAccountRetrieveView.as_view()),
    re_path(r"^AccountOwnerRetrieve/(?P<nationalCode>\d+)$", GetAccountOwnerDataView.as_view()),

]
