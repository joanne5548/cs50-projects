# Generated by Django 5.1.4 on 2024-12-23 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_remove_auction_closed_auction_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='content',
        ),
    ]
