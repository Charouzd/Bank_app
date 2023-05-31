from django.db import models
from django.contrib.auth.models import User
class Transaction(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    direction = models.CharField(max_length=3, choices=[('in', 'In'), ('out', 'Out')])
    currency = models.CharField(max_length=5)
    amount = models.FloatField(default=0)
    status = models.BooleanField(default=False)
    objects = models.Manager()
    def __str__(self):
        # st="Transaction id {self.pk}:"
        # if {self.direction.upper.__eq__("in")}:
        #     st+=" + "
        # else:
        #     st+=" - "
        #     st+=(str)({self.amount})+" "+{self.currency}
        # if{self.status}:
        #     st+="was "
        # return f"Transaction id {self.pk}  Account: {self.account}, Direction: {self.direction}, Currency: {self.currency}, Amount: {self.amount}, Status: {self.status}"
        
        st = "Transaction id " + str(self.pk) + ": "
        if self.direction == "in":
            st += "+ "
        else:
            st += "- "
        st += str(self.amount) + " " + self.currency
        if self.status:
            st += " was successful"
        else:
            st += " failed"
        return (str)(st)