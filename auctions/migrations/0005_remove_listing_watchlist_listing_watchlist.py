# Generated by Django 4.2.14 on 2024-07-27 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_watchlist_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.BooleanField(default=False),
        ),
    ]