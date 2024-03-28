from django.db import models
from django.utils import timezone

# Create your models here.


class Coupon(models.Model):
    id = models.BigAutoField(primary_key=True)
    coupon_name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    # image = models.ImageField(blank=True, upload_to="images/",null=True)
    is_expired = models.BooleanField(default=True)
    discount = models.IntegerField(default=10)
    minimum_amount = models.IntegerField(default=500)
    start_time = models.DateTimeField(default=timezone.now)
    expiration_time = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    msg = models.TextField(null=True)
    # is_one_time_use = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     # Check if expiration time has passed
    #     if self.expiration_time < timezone.now():
    #         self.is_expired = False
    #     super().save(*args, **kwargs)
