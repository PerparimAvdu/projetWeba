# Generated by Django 3.2.7 on 2021-10-02 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations_management', '0033_alter_reservation_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Pursuit', 'Pursuit'), ('Canceled', 'Canceled')], max_length=200, null=True)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('basic_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('extra_kms', models.IntegerField(blank=True, null=True)),
                ('extra_time', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('extra_for_accident', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='invoice',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations_management.invoice'),
        ),
    ]
