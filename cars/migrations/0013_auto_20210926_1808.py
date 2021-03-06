# Generated by Django 3.2.7 on 2021-09-26 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0012_price_category_kms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price_options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hoursDriving', models.CharField(blank=True, max_length=100, null=True)),
                ('kms', models.CharField(blank=True, max_length=10, null=True)),
                ('price', models.CharField(blank=True, max_length=10, null=True)),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.car')),
            ],
        ),
        migrations.DeleteModel(
            name='Price',
        ),
        migrations.DeleteModel(
            name='Price_category',
        ),
    ]
