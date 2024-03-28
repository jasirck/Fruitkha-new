from django.db import models
from login.models import Customer


# Create your models here.
class Wallet(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="Wallet_user"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Wallet_list(models.Model):
    id = models.BigAutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="Wallet")
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_credit = models.BooleanField()
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    msg = models.TextField(null=True)
