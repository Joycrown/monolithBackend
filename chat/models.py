import time
import random
import string

from datetime import datetime
from core.models import User
from utils.utils import get_random_code

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
# TODO Add News


def upload_to(instance, filename):
    return 'messages/{filename}'.format(filename=filename)


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin', editable=True)
    name = models.CharField(max_length=1000, blank=True)
    slug = models.SlugField(max_length=1000, blank=True)
    tos = models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        ex = False
        if self.name:
            to_slug = slugify(str(self.name))
            ex = Admin.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + "" + str(get_random_code()))
                ex = Admin.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.name)
        self.slug = to_slug
        super().save(*args, **kwargs)


class GenericFileUpload(models.Model):
    file_upload = models.FileField(upload_to=upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_upload}"


class Message(models.Model):
    sender = models.ForeignKey(
        "core.User", related_name="admin_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        "core.User", related_name="admin_receiver", on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"message between {self.sender.username} and {self.receiver.username}"

    class Meta:
        ordering = ("-created_at",)


class MessageAttachment(models.Model):
    message = models.ForeignKey(
        Message, related_name="message_attachments", on_delete=models.CASCADE)
    attachment = models.ForeignKey(
        GenericFileUpload, related_name="message_uploads", on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
