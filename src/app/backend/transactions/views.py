from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import BitcoinTransaction
from .serializers import BitcoinTransactionSerializer


class BitcoinTransactionListCreate(generics.ListCreateAPIView):
    serializer_class = BitcoinTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return BitcoinTransaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)


class BitcoinTransactionDelete(generics.DestroyAPIView):
    serializer_class = BitcoinTransactionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return BitcoinTransaction.objects.filter(user=self.request.user)


class BitcoinTransactionUpdate(generics.UpdateAPIView):
    queryset = BitcoinTransaction.objects.all()
    serializer_class = BitcoinTransactionSerializer
    lookup_field = "pk"
