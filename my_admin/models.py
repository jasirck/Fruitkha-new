from django.db import models
from django.utils import timezone


# from image_cropping import ImageRatioField
# Create your models here.
class AdminCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    category_description = models.TextField()
    offer = models.IntegerField()
    category_image = models.ImageField(
        upload_to="category_image/",
    )
    status = models.CharField(max_length=50, default="list")
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class myvariant(models.Model):
    id = models.BigAutoField(primary_key=True)
    variant_name = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50, default="list")
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.variant_name


class myprodect(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=10, default="list")
    price = models.IntegerField()
    prodect_name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        AdminCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_products",
    )
    description = models.TextField()
    quantity = models.IntegerField()
    variant = models.ForeignKey(
        myvariant, on_delete=models.SET_NULL, null=True, related_name="variant_products"
    )
    date_added = models.DateTimeField(default=timezone.now)
    offer = models.IntegerField(null=True)
    rating = models.FloatField(default=3.5)
    prodect_image1 = models.ImageField(upload_to="image/")
    prodect_image2 = models.ImageField(upload_to="image/")
    prodect_image3 = models.ImageField(upload_to="image/")
    # cropping = ImageRatioField('image', '225x225')

    def __str__(self):
        return self.prodect_name
