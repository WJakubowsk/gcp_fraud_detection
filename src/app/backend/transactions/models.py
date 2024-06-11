from django.contrib.auth.models import User
from django.db import models


class BitcoinTransaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    tx_id = models.IntegerField(null=False, blank=False)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(null=False, blank=False)
    description = models.CharField(null=False, blank=True, max_length=255)
    isFraud = models.BooleanField(default=None, null=True)
    isConfirmed = models.BooleanField(default=None, null=True)

    for i in range(93):
        exec(
            f"Local_feature_{i + 1} = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='Local Feature {i + 1}')"
        )

    for i in range(72):
        exec(
            f"Aggregate_feature_{i + 1} = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='Aggregate Feature {i + 1}')"
        )

    for feature in ["in_txs_degree", "out_txs_degree"]:
        exec(
            f"{feature} = models.IntegerField(null=True, blank=True, verbose_name='{feature}')"
        )

    for feature in ["total_BTC", "fees", "size"]:
        exec(
            f"{feature} = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='{feature}')"
        )

    for feature in [
        "in_BTC_min",
        "in_BTC_max",
        "in_BTC_mean",
        "in_BTC_median",
        "in_BTC_total",
        "out_BTC_min",
        "out_BTC_max",
        "out_BTC_mean",
        "out_BTC_median",
        "out_BTC_total",
    ]:
        exec(
            f"{feature} = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name='{feature}')"
        )

    for feature in ["num_input_addresses", "num_output_addresses"]:
        exec(
            f"{feature} = models.IntegerField(null=True, blank=True, verbose_name='{feature}')"
        )

    def __str__(self):
        return str(self.user) + " - " + str(self.amount) + " - " + str(self.date)
