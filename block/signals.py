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
        
