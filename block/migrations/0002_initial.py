# Generated by Django 3.2.7 on 2022-12-26 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('block', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rule',
            name='block',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='block.block'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='block.block'),
        ),
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alt', to='block.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='report',
            field=models.ManyToManyField(blank=True, default=None, related_name='post_report', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='saved',
            field=models.ManyToManyField(blank=True, default=None, related_name='post_saved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='voters',
            field=models.ManyToManyField(related_name='post_voters', through='block.Vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='link',
            name='block',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='block.block'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='block.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='block.post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='report',
            field=models.ManyToManyField(blank=True, default=None, related_name='comment_report', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='saved',
            field=models.ManyToManyField(blank=True, default=None, related_name='comment_saved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='voters',
            field=models.ManyToManyField(related_name='comment_voters', through='block.Vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='block',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='block',
            name='moderators',
            field=models.ManyToManyField(blank=True, default=None, related_name='moderators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='block',
            name='subscribers',
            field=models.ManyToManyField(blank=True, default=None, related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
