# Generated by Django 3.2.12 on 2024-03-06 17:21

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Wallet",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("date", models.DateTimeField(auto_now=True)),
                ("total_ammount", models.DecimalField(decimal_places=2, max_digits=5)),
                ("ammount", models.DecimalField(decimal_places=2, max_digits=7)),
                ("reason", models.CharField(max_length=50)),
            ],
        ),
    ]
