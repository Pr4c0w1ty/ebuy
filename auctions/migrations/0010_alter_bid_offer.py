# Generated by Django 4.2.14 on 2024-07-30 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_bid_bid_listing_remove_bid_is_biddable_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='offer',
            field=models.FloatField(default=0),
        ),
    ]
