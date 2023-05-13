from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    CZK = models.IntegerField(default=0)
    Currencies=models.JSONField(default=dict)
    objects = models.Manager()