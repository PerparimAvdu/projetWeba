# Generated by Django 3.2.7 on 2021-09-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations_management', '0032_alter_reservation_selected_hours_kms_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(blank=True, choices=[('Confirmed', 'Confirmed'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], max_length=200, null=True),
        ),
    ]
