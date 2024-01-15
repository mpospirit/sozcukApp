# Generated by Django 4.2.3 on 2023-07-28 18:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_visitors_agent_alter_competitors_datecreated'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitors',
            name='csrfCookie',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='competitors',
            name='dateCreated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 28, 21, 31, 22, 246807)),
        ),
        migrations.AlterField(
            model_name='visitors',
            name='dateCreated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 7, 28, 21, 31, 22, 246807)),
        ),
    ]