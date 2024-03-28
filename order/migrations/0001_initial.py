# Generated by Django 3.2.12 on 2024-03-02 12:54

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("my_admin", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="order",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("address", models.TextField()),
                ("total_price", models.FloatField()),
                ("payment_method", models.CharField(max_length=150)),
                ("payment_id", models.CharField(max_length=250, null=True)),
                ("status", models.CharField(default="Pending", max_length=150)),
                ("msg", models.TextField(null=True)),
                ("order_id", models.CharField(max_length=150, null=True)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "expect",
                    models.DateField(
                        default=datetime.datetime(
                            2024, 3, 8, 12, 54, 35, 387912, tzinfo=utc
                        )
                    ),
                ),
                ("updated", models.DateField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="order_items",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price_now", models.FloatField()),
                ("quantity_now", models.IntegerField()),
                (
                    "order_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="order.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="my_admin.myprodect",
                    ),
                ),
            ],
        ),
    ]
