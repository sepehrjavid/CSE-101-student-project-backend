from django.urls import path

from transaction.views import TransactionListCreateView

app_name = "transaction"

urlpatterns = [
    path("TransactionListCreate", TransactionListCreateView.as_view())
]
