# Generated by Django 3.2.7 on 2021-09-26 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0015_auto_20210926_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='unlimited_kms',
        ),
    ]
