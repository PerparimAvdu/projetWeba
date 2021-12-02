# Generated by Django 3.2.7 on 2021-09-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0014_auto_20210926_1820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price_category',
            old_name='hoursDriving',
            new_name='hours',
        ),
        migrations.RemoveField(
            model_name='price_category',
            name='kms',
        ),
        migrations.AddField(
            model_name='price',
            name='kms',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='unlimited_kms',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
