# Generated by Django 4.2.4 on 2023-08-16 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_remove_listing_bid_bid_listing_listing_buyer_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="publisher",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="listings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
