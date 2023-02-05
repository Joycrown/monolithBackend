# Generated by Django 3.2.7 on 2023-02-05 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0009_auto_20230205_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=300),
        ),
    ]
