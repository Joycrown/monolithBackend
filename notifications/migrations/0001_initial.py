# Generated by Django 3.2.7 on 2023-05-04 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('block', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('C', 'comment'), ('P', 'post'), ('RP', 'repost'), ('VP', 'vote_post'), ('VC', 'vote_comment'), ('F', 'follow'), ('UF', 'unfollow'), ('CT', 'chat')], max_length=20)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_has_seen', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='block.comment')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='block.post')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
