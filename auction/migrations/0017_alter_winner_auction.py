# Generated by Django 5.0.6 on 2024-06-26 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0016_rename_winning_price_winner_winning_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='auction',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auction.auction'),
        ),
    ]
