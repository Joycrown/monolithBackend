import time
import random
import string

from django.db import models, transaction
from django.db.models import Sum
from django.conf import settings
from django.core.exceptions import FieldError
from django.contrib.auth.models import Permission
from django.utils.text import slugify
from django.utils import timezone

from guardian.shortcuts import assign_perm
from datetime import datetime, timedelta
from utils.utils import get_random_code
from PIL import Image

from core.models import User
#TODO Add more details to block, posts, comments


def link_to(instance, filename):
    return 'links/{0}/{1}'.format(instance.title, filename)

def post_to(instance, filename):
    return 'posts/{0}/{1}'.format(instance.title, filename)

def block_to(instance, filename):
    return 'avatars/{0}/{1}'.format(instance.name, filename)

def block_for(instance, filename):
    return 'covers/{0}/{1}'.format(instance.name, filename)

def get_perm(codename):
    return Permission.objects.get(content_type__app_label='pyramid', codename=codename)

def get_model_perms():
    perms = []
    for op in ['change', 'delete']:
        for model_name in ['comment', 'post']:
            perms.append(get_perm(f'{op}_{model_name}'))
    return perms

def pluralize(value, unit):
    if value == 1:
        return f'1{unit}'
    return f'{value}{unit}'

def time_ago(dt):
    t = timezone.now() - dt
    if t.days == 0:
        if t.seconds < 60:
            return 'just now'
        if t.seconds < 3600:
            return pluralize(t.seconds//60, 'm')
        if t.seconds < 3600 * 24:
            return pluralize(t.seconds//3600, 'h')
    if t.days < 30:
        return pluralize(t.days, 'd')
    if t.days < 365:
        return pluralize(t.days//30, 'mo')
    return pluralize(t.days//365, 'yr')


def pluralize(value, unit):
    if value == 1:
        return f'1{unit}'
    return f'{value}{unit}'

def time_ago(dt):
    t = timezone.now() - dt
    if t.days == 0:
        if t.seconds < 60:
            return 'just now'
        if t.seconds < 3600:
            return pluralize(t.seconds//60, 'm')
        if t.seconds < 3600 * 24:
            return pluralize(t.seconds//3600, 'h')
    if t.days < 30:
        return pluralize(t.days, 'd')
    if t.days < 365:
        return pluralize(t.days//30, 'mo')
    return pluralize(t.days//365, 'yr')

def edited(model):
    # The text object is created first so if the comment/post is unedited
    # the last_modified will be before the created
    # Maybe created should be an attribute of the text model
    td = (model.text.last_modified - model.created)
    return td.days > -1 and td.seconds > 60 * 5


class Text(models.Model):
    text = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class Block(models.Model):
    avatar = models.ImageField(upload_to=block_to, blank=True, null=True, max_length=100000)
    cover = models.ImageField(upload_to=block_for, blank=True, null=True, max_length=100000)
    name = models.CharField(max_length=250, unique=True)
    desc = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=1000, null=True, blank=True)
    block_type = models.CharField(max_length=100, null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers', blank=True, default=None)
    moderators = models.ManyToManyField(User, related_name='moderators', blank=True, default=None)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    created = models.DateTimeField(auto_now_add=True)
    subscriber_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=False)

    @property
    def numPosts(self):
        return self.post_set.all().count()

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return '/b/' + self.name  

    def save(self, *args, **kwargs):
        ex = False
        SIZE = 250, 250
        if self.name:
            to_slug = slugify(str(self.name))
            ex = Block.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + "" + str(get_random_code()))
                ex = Block.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.name)
        self.slug = to_slug
        super().save(*args, **kwargs)


class Link(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, blank=True, default=None)
    image = models.ImageField(upload_to=link_to, blank=True, null=True, max_length=100000)
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True, max_length=2000)
    last_modified = models.DateTimeField(auto_now=True)


class Rule(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, blank=True, default=None)
    title = models.CharField(max_length=300)
    text = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class DeletedUser(object):
    username = '[deleted]'
    def get_username(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=300)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to=post_to, blank=True, null=True, max_length=100000)
    created = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True, max_length=2000)
    text = models.TextField(blank=True, null=True)
    post_type = models.CharField(max_length=300, blank=True, null=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="alt")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    report = models.ManyToManyField(User, related_name="post_report", blank=True, default=None)
    saved = models.ManyToManyField(User, related_name="post_saved", blank=True, default=None)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    saved_count = models.IntegerField(blank=True, null=True, default=0)
    report_count = models.IntegerField(blank=True, null=True, default=0)
    is_deleted = models.BooleanField(default=False)
    is_repost = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=True)
    voters = models.ManyToManyField(User, through='Vote', through_fields=('post', 'voter'), related_name='post_voters')
    votes = models.IntegerField(default=0)
    reposts = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)    
    slug = models.SlugField(blank=True, null=False)

    def get_author(self):
        if self.is_deleted:
            return DeletedUser()
        return self.author

    @property
    def top_comments(self):
        return self.comment_set.order_by('votes')

    @property
    def new_comments(self):
        return self.comment_set.order_by('created')

    @property
    def old_comments(self):
        return self.comment_set.order_by('-created')

    @property
    def created_time_ago(self):
        return time_ago(self.created)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        new_record = self.pk is None
        with transaction.atomic():
            super(Post, self).save(*args, **kwargs)
            if new_record:
                Vote.objects.create(voter=self.author, value=1, post=self)
                assign_perm('block.change_post', self.author, self)
                assign_perm('block.delete_post', self.author, self)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return '/b/' + self.block.name + ' -- ' + self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True , blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank=True)
    report = models.ManyToManyField(User, related_name="comment_report", blank=True, default=None)
    saved = models.ManyToManyField(User, related_name="comment_saved", blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    saved_count = models.IntegerField(blank=True, null=True, default=0)
    report_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    voters = models.ManyToManyField(User, through='Vote', through_fields=('comment', 'voter'), related_name='comment_voters')
    votes = models.IntegerField(default=0)

    def get_author(self):
        if self.is_deleted:
            return DeletedUser()
        return self.author

    @property
    def saved_count(self):
        return self.saved.all().count()

    @property
    def report_count(self):
        return self.report.all().count()

    @property
    def child_comments(self):
        return self.comment_set.all().order_by('-votes', 'created')

    @property
    def created_time_ago(self):
        return time_ago(self.created)

    def save(self, *args, **kwargs):
        new_record = self.pk is None
        with transaction.atomic():
            super(Comment, self).save(*args, **kwargs)
            if new_record:
                Vote.objects.create(voter=self.author, value=1, comment=self)
                assign_perm('block.change_comment', self.author, self)
                assign_perm('block.delete_comment', self.author, self)

    def __str__(self):
        if len(self.text) < 20:
            return self.text
        return self.text[:20] + '...'

    
class VoteManager(models.Manager):
    def create(self, voter, value, post=None, comment=None):
        vote = self.model(
            voter=voter,
            value=value,
            is_post=bool(post),
            is_comment=bool(comment),
            post=post,
            comment=comment
        )
        vote.save()
        return vote

class Vote(models.Model):
    voter = models.ForeignKey(User, related_name='voter', on_delete=models.CASCADE)
    value = models.IntegerField() # should be -1 or 1
    is_post = models.BooleanField()
    is_comment = models.BooleanField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    objects = VoteManager()

    def validate(self):
        if self.value not in [-1, 1]:
            raise FieldError('value must be in [-1, 1]')
        if self.post is None and self.comment is None:
            raise FieldError('post and comment cannot both be null')
        if self.post and self.comment:
            raise FieldError('cannot submit vote for both post and comment')
        if self.pk is None and self.post and self.voter in self.post.voters.all():
            raise FieldError('voter has already voted on this post')
        if self.pk is None and self.comment and self.voter in self.comment.voters.all():
            raise FieldError('voter has already voted on this comment')
        return True

    def save(self, *args, **kwargs):
        self.validate()
        with transaction.atomic():
            super(Vote, self).save(*args, **kwargs)
            if self.comment:
                value__sum = self.comment.vote_set.aggregate(Sum('value'))
                self.comment.votes = value__sum['value__sum']
                self.comment.save()
            if self.post:
                value__sum = self.post.vote_set.aggregate(Sum('value'))
                self.post.votes = value__sum['value__sum']
                self.post.save()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.comment:
                self.comment.votes -= self.value
                self.comment.save()
            if self.post:
                self.post.votes -= self.value
                self.post.save()
            super(Vote, self).delete(*args, **kwargs)
