# Generated by Django 3.2.7 on 2023-11-04 13:27

import chamber.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=33)),
                ('message_handler', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chamber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, max_length=1000000, null=True, upload_to=chamber.models.chamber_to)),
                ('cover', models.ImageField(blank=True, max_length=1000000, null=True, upload_to=chamber.models.chamber_for)),
                ('room_code', models.CharField(max_length=8)),
                ('room_name', models.CharField(max_length=255)),
                ('day', models.CharField(blank=True, max_length=1000, null=True)),
                ('month', models.CharField(blank=True, max_length=1000, null=True)),
                ('year', models.CharField(blank=True, max_length=1000, null=True)),
                ('about', models.TextField(blank=True, max_length=100000, null=True)),
                ('subscriber_count', models.IntegerField(blank=True, default=0, null=True)),
                ('category', models.CharField(blank=True, max_length=1000, null=True)),
                ('chamber_type', models.CharField(blank=True, max_length=100, null=True)),
                ('share_count', models.IntegerField(blank=True, default=0, null=True)),
                ('active_bots', models.ManyToManyField(to='chamber.Bot')),
                ('blocked_users', models.ManyToManyField(related_name='blocked_users_set', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('moderator_users', models.ManyToManyField(related_name='moderator_users_set', to=settings.AUTH_USER_MODEL)),
                ('subscribed_users', models.ManyToManyField(related_name='subscribed_users_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_agent', models.TextField(null=True)),
                ('ip_addr', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, max_length=1000000, null=True, upload_to=chamber.models.file_to)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('day', models.CharField(blank=True, max_length=3, null=True)),
                ('month', models.CharField(blank=True, max_length=15, null=True)),
                ('year', models.CharField(blank=True, max_length=7, null=True)),
                ('time', models.CharField(blank=True, max_length=15, null=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chamber.chamber')),
            ],
        ),
    ]
