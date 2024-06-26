# Generated by Django 5.0.6 on 2024-06-04 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0011_auctionrequest_auction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionrequest',
            name='auction',
        ),
        migrations.RemoveField(
            model_name='auctionrequest',
            name='product',
        ),
        migrations.AddField(
            model_name='auction',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionrequest',
            name='admin_message',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='auctionrequest',
            name='Auction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auction.auction'),
        ),
    ]
