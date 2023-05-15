from django.db import models
from django.contrib.auth.models import User
class Transaction(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    direction = models.CharField(max_length=3, choices=[('in', 'In'), ('out', 'Out')])
    currency = models.CharField(max_length=5)
    amount = models.FloatField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction {self.pk}"
