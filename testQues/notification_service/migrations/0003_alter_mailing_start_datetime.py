# Generated by Django 4.2.1 on 2023-05-20 18:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification_service', '0002_alter_mailing_start_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 21, 50, 4, 110809)),
        ),
    ]
