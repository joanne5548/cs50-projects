# Generated by Django 5.1.4 on 2024-12-21 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_image_url_auction_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='img_url',
            field=models.URLField(blank=True),
        ),
    ]
