from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "", views.BitcoinTransactionListCreate.as_view(), name="transaction_list_create"
    ),
    path(
        "delete/<int:pk>/",
        views.BitcoinTransactionDelete.as_view(),
        name="transaction_delete",
    ),
    path(
        "update/<int:pk>/",
        views.BitcoinTransactionUpdate.as_view(),
        name="transaction_update",
    ),
    path(
        "predict/<int:pk>/",
        views.BitcoinTransactionPredict.as_view(),
        name="transaction_predict",
    ),
    path(
        "predict-all/",
        views.BitcoinTransactionPredictAll.as_view(),
        name="transaction_predict_all",
    ),
    path(
        "retrieve/<int:pk>/",
        views.BitcoinTransactionRetrieve.as_view(),
        name="transaction_retrieve",
    ),
]
