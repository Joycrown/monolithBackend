# Generated by Django 3.2.7 on 2022-12-29 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0003_auto_20221228_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reposts',
            field=models.IntegerField(default=0),
        ),
    ]
