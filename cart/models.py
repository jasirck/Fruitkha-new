from django.db import models
from my_admin.models import myprodect
from login.models import Customer


# Create your models here.
class cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(myprodect, on_delete=models.CASCADE)
    book_quantity = models.IntegerField(null=True)
    cart_total = models.IntegerField()
    current_price = models.IntegerField(null=True)


class Wishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="wishlist_users"
    )
    product_id = models.ForeignKey(
        myprodect, on_delete=models.CASCADE, related_name="wishlist_products"
    )
