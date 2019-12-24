from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import BankAccount, AccountOwner
from accounts.serializers import BankAccountSerializer, UserLoginSerializer, BankAccountNumberSerializer, \
    AccountLogSerializer, AddAccountToAccountOwnerSerializer, AccountOwnerSerializer


class BankAccountListCreateView(ListCreateAPIView):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()
    permission_classes = [IsAuthenticated]


class BankAccountRetrieveView(RetrieveAPIView):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "accountNumber"


class SignUpView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class GetBankAccountLogsView(APIView):
    serializer_class = BankAccountNumberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = BankAccountNumberSerializer(data=request.data)
        if ser.is_valid():
            account = get_object_or_404(BankAccount, accountNumber=ser.validated_data.get("accountNumber"))
            output = {
                "currentCredit": account.credit,
                "logs": AccountLogSerializer(account.logs, many=True).data,
            }
            return Response(output, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class AddAccountToAccountOwnerView(APIView):
    serializer_class = AddAccountToAccountOwnerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = AddAccountToAccountOwnerSerializer(data=request.data)
        if ser.is_valid():
            nationalCode = ser.validated_data.get("nationalCode")
            owner = get_object_or_404(AccountOwner, nationalCode=nationalCode)
            account = BankAccount.objects.create(accountOwner=owner, accountNumber=BankAccount.createAccountNumber())
            return Response(BankAccountSerializer(account).data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAccountOwnerDataView(RetrieveAPIView):
    serializer_class = AccountOwnerSerializer
    queryset = AccountOwner.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "nationalCode"


class CloseAccountView(APIView):
    serializer_class = BankAccountNumberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = BankAccountNumberSerializer(data=request.data)
        if ser.is_valid():
            account = get_object_or_404(BankAccount, accountNumber=ser.validated_data.get("accountNumber"))
            account.status = "C"
            account.save()
            return Response("ok", status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockAccountView(APIView):
    serializer_class = BankAccountNumberSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = BankAccountNumberSerializer(data=request.data)
        if ser.is_valid():
            account = get_object_or_404(BankAccount, accountNumber=ser.validated_data.get("accountNumber"))
            account.status = "B"
            account.save()
            return Response("ok", status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
