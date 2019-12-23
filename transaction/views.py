from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class TransactionListCreateView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

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
