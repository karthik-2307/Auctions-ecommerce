# Generated by Django 4.2.1 on 2023-06-09 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_bid_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_closed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
