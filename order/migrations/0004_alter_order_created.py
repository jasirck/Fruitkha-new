# Generated by Django 3.2.12 on 2024-03-07 09:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0003_alter_order_expect"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="created",
            field=models.DateTimeField(auto_now=True),
        ),
    ]