# Generated by Django 5.1.4 on 2024-12-22 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auction_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='closed',
        ),
        migrations.AddField(
            model_name='auction',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
