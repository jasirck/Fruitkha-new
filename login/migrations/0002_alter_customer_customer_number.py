# Generated by Django 3.2.12 on 2024-03-02 08:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("login", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="customer_number",
            field=models.BigIntegerField(null=True),
        ),
    ]
