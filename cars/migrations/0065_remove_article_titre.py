# Generated by Django 4.0.1 on 2022-01-25 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0064_article_titre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='Titre',
        ),
    ]
