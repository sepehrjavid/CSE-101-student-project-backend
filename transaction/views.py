from rest_framework.generics import ListCreateAPIView

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class TransactionListCreateView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.fromAccount is not None:
            instance.fromAccount.createLog(instance.amount,
                                           instance.definition,
                                           "-")
        if instance.toAccount is not None:
            instance.toAccount.createLog(instance.amount,
                                         instance.definition,
                                         "+")
