# Generated by Django 2.2.24 on 2021-10-31 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations_management', '0049_alter_reservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='date_location_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
