# Generated by Django 3.2.12 on 2024-03-10 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0003_alter_wishlist_product_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="current_price",
            field=models.IntegerField(null=True),
        ),
    ]
