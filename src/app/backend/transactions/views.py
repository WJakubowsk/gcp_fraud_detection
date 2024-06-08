import os

import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


class BitcoinTransactionPredict(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            transaction = BitcoinTransaction.objects.get(pk=pk, user=request.user)
        except BitcoinTransaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)

        prediction_url = os.environ["PREDICTION_URL"]

        response = requests.post(prediction_url, json={"indices": [transaction.tx_id]})

        if response.status_code == 200:
            prediction_result = response.json()

            if prediction_result["predictions"][0] == 0.0:
                transaction.isFraud = False
            elif prediction_result["predictions"][0] == 1.0:
                transaction.isFraud = True
            transaction.save()

            return Response(prediction_result)
        else:
            return Response(
                {"error": "Prediction API error"}, status=response.status_code
            )


class BitcoinTransactionPredictAll(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        transactions = BitcoinTransaction.objects.filter(
            user=request.user, isFraud__isnull=True
        )
        if not transactions.exists():
            return Response({"message": "No transactions to predict"}, status=204)

        payload = {"indices": [transaction.tx_id for transaction in transactions]}

        prediction_url = os.environ["PREDICTION_URL"]

        try:
            response = requests.post(prediction_url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=500)

        prediction_results = response.json().get("predictions", [])
        if not prediction_results:
            return Response({"error": "No predictions received"}, status=500)

        updated_transactions = []
        for i, transaction in enumerate(transactions):
            res = prediction_results[i]
            transaction.isFraud = False if res == 0.0 else True
            transaction.save()
            updated_transactions.append(transaction)

        serializer = BitcoinTransactionSerializer(updated_transactions, many=True)
        return Response(serializer.data, status=200)
