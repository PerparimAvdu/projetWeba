# Generated by Django 3.2.7 on 2021-09-26 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0016_remove_price_unlimited_kms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='kms',
        ),
        migrations.AddField(
            model_name='price_category',
            name='kms',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
