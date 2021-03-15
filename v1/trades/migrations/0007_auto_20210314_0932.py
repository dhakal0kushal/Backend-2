# Generated by Django 3.1.6 on 2021-03-14 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0006_auto_20210310_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traderequest',
            name='is_accepted',
        ),
        migrations.AddField(
            model_name='traderequest',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Rejected')], default=0),
            preserve_default=False,
        ),
    ]