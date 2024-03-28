# Generated by Django 3.2.12 on 2024-03-09 09:57

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category_Offer",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("percentage", models.FloatField(blank=True, default=0, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product_Offer",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("percentage", models.FloatField(blank=True, default=0, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
    ]