# Generated by Django 3.2.7 on 2023-02-05 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0008_auto_20230204_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='about',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='desc',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
    ]
