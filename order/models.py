from django.db import models
from login.models import Customer
from my_admin.models import myprodect
from django.utils import timezone
from coupon.models import Coupon
# Create your models here.


def default_expect_date():
    return timezone.now() + timezone.timedelta(days=6)


class order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_method = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    status = models.CharField(max_length=150, null=False, default="Ordered")
    msg = models.TextField(null=True)
    order_id = models.CharField(max_length=150, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    expect = models.DateField(default=default_expect_date)
    updated = models.DateField(auto_now=True)
    coupon_id = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)


class order_items(models.Model):
    order_item = models.ForeignKey(order, on_delete=models.CASCADE)
    product = models.ForeignKey(myprodect, on_delete=models.CASCADE)
    price_now = models.FloatField()
    quantity_now = models.IntegerField()
