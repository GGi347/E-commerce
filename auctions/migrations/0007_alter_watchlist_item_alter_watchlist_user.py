# Generated by Django 4.0.3 on 2022-03-09 05:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auction_listing_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='item',
            field=models.ManyToManyField(related_name='wishlist', to='auctions.auction_listing'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.ManyToManyField(related_name='wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
