# Generated by Django 4.0.3 on 2022-03-09 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_watchlist_item_alter_watchlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='addec_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]