# Generated by Django 5.0.6 on 2024-10-30 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_reservation_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='is_active',
        ),
    ]
