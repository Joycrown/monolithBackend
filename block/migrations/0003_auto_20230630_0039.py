# Generated by Django 3.2.7 on 2023-06-29 23:39

import block.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='avatar',
            field=models.ImageField(blank=True, max_length=1000000, null=True, upload_to=block.models.block_to),
        ),
        migrations.AlterField(
            model_name='block',
            name='cover',
            field=models.ImageField(blank=True, max_length=1000000, null=True, upload_to=block.models.block_for),
        ),
    ]
