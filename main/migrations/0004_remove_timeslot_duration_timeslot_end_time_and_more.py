# Generated by Django 5.0.1 on 2024-07-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_booking_building_eveningdate_room_subject_teacher_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='duration',
        ),
        migrations.AddField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='eveningdate',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
