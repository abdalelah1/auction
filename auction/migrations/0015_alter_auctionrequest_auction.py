# Generated by Django 5.0.6 on 2024-06-06 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0014_alter_auctionrequest_auction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionrequest',
            name='Auction',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='auction.auction'),
        ),
    ]
