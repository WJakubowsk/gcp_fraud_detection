from django.contrib.auth.models import User
from django.db import models


class BitcoinTransaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user) + " - " + str(self.amount) + " - " + str(self.date)
