# Generated by Django 3.2.7 on 2021-10-04 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations_management', '0038_auto_20211003_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='hours_kms',
        ),
        migrations.AddField(
            model_name='reservation',
            name='hours',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='kms',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]