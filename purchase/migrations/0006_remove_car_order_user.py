# Generated by Django 3.1.1 on 2020-10-14 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_auto_20201014_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car_order',
            name='user',
        ),
    ]
