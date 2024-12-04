# Generated by Django 5.0.1 on 2024-08-20 14:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_booking_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_id',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]