# Generated by Django 4.2 on 2025-02-23 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0009_customcake_custom_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
