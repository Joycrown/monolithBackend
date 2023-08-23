# Generated by Django 3.2.7 on 2023-08-23 23:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(default='description')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('preview', models.ImageField(blank=True, max_length=1000000, null=True, upload_to=events.models.event_for)),
                ('type', models.CharField(default='PRIVATE', max_length=100)),
                ('code_adhesion', models.CharField(default='', max_length=20)),
                ('category', models.CharField(default='', max_length=20000)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2023, 8, 24, 0, 34, 19, 147306), verbose_name='start_date')),
                ('end_date', models.DateTimeField(default=datetime.datetime(2023, 8, 24, 0, 34, 19, 147306, tzinfo=utc), verbose_name='end_date')),
                ('end_date_inscription', models.DateTimeField(verbose_name='end_date_inscription')),
                ('status', models.CharField(default='ACTIVE', max_length=100)),
                ('location', models.CharField(default='online', max_length=255)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='STATUS', max_length=255)),
                ('feedback', models.TextField(default='feedback')),
                ('rating', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='guests',
            field=models.ManyToManyField(related_name='guests', through='events.Guest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
