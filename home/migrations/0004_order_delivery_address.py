# Generated by Django 5.1.2 on 2024-10-22 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_comment_user_remove_rating_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
