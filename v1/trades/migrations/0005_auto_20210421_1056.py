# Generated by Django 3.1.7 on 2021-04-21 05:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0001_initial'),
        ('trades', '0004_auto_20210421_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedtrade',
            name='payment_method',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='constants.paymentmethod'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='completedtrade',
            name='rate',
            field=models.PositiveIntegerField(default=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='traderequest',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 22, 5, 11, 9, 225297, tzinfo=utc)),
        ),
    ]