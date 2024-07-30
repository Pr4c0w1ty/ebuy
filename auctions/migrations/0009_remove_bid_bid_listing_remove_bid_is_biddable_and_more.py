# Generated by Django 4.2.14 on 2024-07-28 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_comment_author_alter_comment_listing_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bid_listing',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='is_biddable',
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.bid'),
        ),
    ]
