# Generated by Django 3.2.7 on 2023-02-05 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0007_alter_post_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='day',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='month',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='year',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
