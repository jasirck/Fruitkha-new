# Generated by Django 3.2.12 on 2024-03-10 07:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("offer", "0002_auto_20240309_1533"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category_offer",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="category_offer",
            name="start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product_offer",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="product_offer",
            name="start_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
