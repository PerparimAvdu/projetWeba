# Generated by Django 3.2.7 on 2021-09-26 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_auto_20210926_1713'),
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