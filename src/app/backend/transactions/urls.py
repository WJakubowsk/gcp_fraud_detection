from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.BitcoinTransactionListCreate.as_view(), name="transaction_list_create"),
    path("delete/<int:pk>/", views.BitcoinTransactionDelete.as_view(), name="transaction_delete"),
]
