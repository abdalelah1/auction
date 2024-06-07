# Generated by Django 5.0.6 on 2024-05-19 09:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0005_remove_auction_starting_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bid_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auction.auction')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auction.customer')),
            ],
        ),
    ]