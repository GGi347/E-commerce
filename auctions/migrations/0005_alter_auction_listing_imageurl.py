# Generated by Django 4.0.3 on 2022-03-08 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='imageUrl',
            field=models.URLField(blank=True, null=True),
        ),
    ]
