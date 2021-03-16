# Generated by Django 3.1.7 on 2021-03-16 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatThread',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('admin_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dispute_threads', to=settings.AUTH_USER_MODEL)),
                ('primary_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_threads', to=settings.AUTH_USER_MODEL)),
                ('secondary_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scondary_threads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]