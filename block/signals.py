from datetime import date
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from django.utils import timezone
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from .models import Block

@receiver(post_save, sender=Block)
def post_save_block(sender, created, instance, **kwargs):
    block = instance
    creator = block.creator
    if created:
        block.moderators.add(creator)
        block.subscribers.add(creator)
        block.subscriber_count =+ 1
        block.save()
        
@receiver(post_save, sender=Block)
def update_user(sender, instance, created, **kwargs):
    block = instance
    now = date.today()
                            
    if created:
        if now.month == 1:
           month = "January"
        elif now.month == 2: 
           month = "February"
        elif now.month == 3: 
           month = "March"
        elif now.month == 4: 
           month = "April"   
        elif now.month == 5: 
           month = "May"
        elif now.month == 6: 
           month = "June" 
        elif now.month == 7: 
           month = "July"
        elif now.month == 8:
           month = "August"   
        elif now.month == 9:
           month = "September" 
        elif now.month == 10: 
           month = "October"
        elif now.month == 11: 
           month = "November" 
        else:
           month = "December"
        block.day = now.day
        block.month = month
        block.year = now.year
        block.save()
