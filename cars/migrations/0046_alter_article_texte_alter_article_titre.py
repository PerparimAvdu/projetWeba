# Generated by Django 4.0.1 on 2022-01-24 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0045_alter_article_texte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Texte',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='Titre',
            field=models.CharField(max_length=100),
        ),
    ]
