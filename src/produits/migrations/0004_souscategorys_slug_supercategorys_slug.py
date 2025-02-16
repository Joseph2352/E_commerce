# Generated by Django 5.1.6 on 2025-02-16 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0003_categorys_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='souscategorys',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='supercategorys',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
