from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Customer(AbstractUser):
    customer_number = models.BigIntegerField(null=True)
    user_dp = models.ImageField(
        upload_to="media/user_dp/", default="media/user_dp/user.jpg"
    )
    current_address = models.ForeignKey(
        "user_address", related_name="address", null=True, on_delete=models.SET_NULL
    )
    action = models.CharField(max_length=10, default="allow")

    class Meta:
        permissions = (("can_view_customer", "Can view customer"),)


# Specify unique related_name for groups and user_permissions fields
Customer._meta.get_field("groups").remote_field.related_name = "customer_groups"
Customer._meta.get_field(
    "user_permissions"
).remote_field.related_name = "customer_permissions"


class user_address(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="user_address"
    )
    name = models.CharField(max_length=50)
    call_number = models.BigIntegerField()
    house_name = models.CharField(max_length=100)
    lanmark = models.CharField(max_length=50)
    post = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
