# Generated by Django 4.0.1 on 2022-01-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0052_remove_article_texte_alter_article_titre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Titre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
