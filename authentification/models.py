from django.db import models
from django.contrib.auth.models import User
from transaction.models import Transaction
# Create your models here.
class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    CZK = models.FloatField(default=(0.0))
    Currencies=models.JSONField(default=dict)
    objects = models.Manager()
    history=models.ManyToManyField(Transaction, related_name='accounts', blank=True)
