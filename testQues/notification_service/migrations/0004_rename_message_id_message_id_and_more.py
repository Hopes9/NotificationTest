# Generated by Django 4.2.1 on 2023-05-20 19:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification_service', '0003_alter_mailing_start_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='message_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='mailing',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 22, 24, 58, 672415)),
        ),
    ]
