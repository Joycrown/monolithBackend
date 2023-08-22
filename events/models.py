import datetime

from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from core.models import User


def event_for(instance, filename):
    return "events/{0}/{1}".format(instance.title, filename)


class Event(models.Model):
    title=models.CharField(max_length=300)
    description=models.TextField(default="description")
    date_created=models.DateTimeField(auto_now_add=True)
    preview=models.ImageField(upload_to=event_for, blank=True, null=True, max_length=1000000)
    type=models.CharField(max_length=100,default="PRIVATE")
    code_adhesion=models.CharField(max_length=20,default="")
    category=models.CharField(max_length=20000,default="")
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name="start_date",default=datetime.datetime.now())
    end_date=models.DateTimeField(verbose_name="end_date", default=(timezone.now() + datetime.timedelta(hours=1)))
    end_date_inscription = models.DateTimeField(verbose_name="end_date_inscription")
    status=models.CharField(max_length=100,default="ACTIVE")
    guests = models.ManyToManyField(User, through='Guest',related_name="guests")
    location = models.CharField(max_length=255,default="online")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255,default="STATUS")
    feedback = models.TextField(default="feedback")
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"Invited {self.user} for {self.event}"

