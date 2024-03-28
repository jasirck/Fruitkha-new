from django.db import models
from my_admin.models import myprodect, AdminCategory
from login.models import Customer

# Create your models here.


class Product_Offer(models.Model):
    id = models.BigAutoField(primary_key=True)
    produc_id = models.ForeignKey(
        myprodect, on_delete=models.CASCADE, null=True, blank=True
    )
    percentage = models.FloatField(null=True, blank=True, default=0)
    start_date = models.DateTimeField(
        null=True, blank=True, auto_now=False, auto_now_add=False
    )
    end_date = models.DateTimeField(
        null=True, blank=True, auto_now=False, auto_now_add=False
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     # Check if expiration time has passed
    #     if self.end_date < timezone.now():
    #         self.is_active = False
    #     super().save(*args, **kwargs)


class Category_Offer(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_id = models.ForeignKey(
        AdminCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    percentage = models.FloatField(null=True, blank=True, default=0)
    start_date = models.DateTimeField(
        null=True, blank=True, auto_now=False, auto_now_add=False
    )
    end_date = models.DateTimeField(
        null=True, blank=True, auto_now=False, auto_now_add=False
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     # Check if expiration time has passed
    #     if self.end_date < timezone.now():
    #         self.is_active = False
    #     super().save(*args, **kwargs)


class Referral(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    code = models.CharField(max_length=250, unique=True)
