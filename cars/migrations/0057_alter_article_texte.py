# Generated by Django 4.0.1 on 2022-01-25 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0056_alter_article_titre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Texte',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
