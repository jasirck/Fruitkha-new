# Generated by Django 3.2.12 on 2024-03-02 06:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AdminCategory",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("category_description", models.TextField()),
                ("offer", models.IntegerField()),
                ("category_image", models.ImageField(upload_to="category_image/")),
                ("status", models.CharField(default="list", max_length=50)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="myvariant",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("variant_name", models.CharField(max_length=255, unique=True)),
                ("status", models.CharField(default="list", max_length=50)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="myprodect",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("status", models.CharField(default="list", max_length=10)),
                ("price", models.IntegerField()),
                ("prodect_name", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField()),
                ("quantity", models.IntegerField()),
                ("offer", models.IntegerField(null=True)),
                ("rating", models.FloatField(default=3.5)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("prodect_image1", models.ImageField(upload_to="image/")),
                ("prodect_image2", models.ImageField(upload_to="image/")),
                ("prodect_image3", models.ImageField(upload_to="image/")),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="category_products",
                        to="my_admin.admincategory",
                    ),
                ),
                (
                    "variant",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="variant_products",
                        to="my_admin.myvariant",
                    ),
                ),
            ],
        ),
    ]
