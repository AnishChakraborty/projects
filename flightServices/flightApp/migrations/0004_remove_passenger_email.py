# Generated by Django 4.0.6 on 2022-07-21 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flightApp', '0003_rename_lastnmae_passenger_lastname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='email',
        ),
    ]
