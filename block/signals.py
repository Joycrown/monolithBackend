from datetime import date
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from django.utils import timezone
from django.dispatch import receiver
from django.db import transaction
from newsdataapi import NewsDataApiClient
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from .models import Block, Post
from core.models import User

@receiver(post_save, sender=Block)
def post_save_block(sender, created, instance, **kwargs):    

    if created:
        block = instance
        creator = block.creator
        block.moderators.add(creator)
        block.subscribers.add(creator)
        block.subscriber_count =+ 1
        block.save()
       
        
@receiver(post_save, sender=Block)
def update_user(sender, instance, created, **kwargs):
    block = instance
    creator = block.creator
    now = date.today()
                            
    if created:
        month = ""
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

@receiver(post_save, sender=Post)
def post_save_create_finance_post(sender, created, instance, **kwargs):    
   api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
   query = "World Economy"
   username = "leox"
   pk = 6
   news = api.news_api(q=query, language="en")
   data = news
   print(data)
   block = get_object_or_404(Block, id=pk)
   author = get_object_or_404(User, username=username)
   if created:
      for new in data.results():
         if new.image_url:
            title = new.title
            attachment = new.image_url
            author = author
            block = block
            post_type = "image"
            Post.objects.create(
                  title=title,
                  attachment=attachment,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.link:
            title = new.title
            link = new.link
            author = author
            block = block
            post_type = "link"
            Post.objects.create(
                  title=title,
                  link=link,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.content:
            title = new.title
            text = new.content
            author = author
            block = block
            post_type = "text"
            Post.objects.create(
                  title=title,
                  text=text,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.video_url:
            title = new.title
            video = new.video_url
            author = author
            block = block
            post_type = "video"
            Post.objects.create(
                  title=title,
                  video=video,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         else:
            pass         

@receiver(post_save, sender=Post)
def post_save_create_crypto_post(sender, created, instance, **kwargs):    
   api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
   query = "Cyptocurrency"
   username = "leox"
   pk = 6
   news = api.news_api(q=query, language="en")
   block = get_object_or_404(Block, id=pk)
   author = get_object_or_404(User, username=username)
   if created:
      for new in news.results():
         if new.image_url:
            title = new.title
            attachment = new.image_url
            author = author
            block = block
            post_type = "image"
            Post.objects.create(
                  title=title,
                  attachment=attachment,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.link:
            title = new.title
            link = new.link
            author = author
            block = block
            post_type = "link"
            Post.objects.create(
                  title=title,
                  link=link,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.content:
            title = new.title
            text = new.content
            author = author
            block = block
            post_type = "text"
            Post.objects.create(
                  title=title,
                  text=text,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.video_url:
            title = new.title
            video = new.video_url
            author = author
            block = block
            post_type = "video"
            Post.objects.create(
                  title=title,
                  video=video,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         else:
            pass

@receiver(post_save, sender=Post)
def post_save_create_stock_post(sender, created, instance, **kwargs):    
   api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
   query = "Stocks"
   username = "Slem"
   pk = 3
   news = api.news_api(q=query, language="en")
   block = get_object_or_404(Block, id=pk)
   author = get_object_or_404(User, username=username)
   if created:
      for new in news.results():
         if new.image_url:
            title = new.title
            attachment = new.image_url
            author = author
            block = block
            post_type = "image"
            Post.objects.create(
                  title=title,
                  attachment=attachment,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.link:
            title = new.title
            link = new.link
            author = author
            block = block
            post_type = "link"
            Post.objects.create(
                  title=title,
                  link=link,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.content:
            title = new.title
            text = new.content
            author = author
            block = block
            post_type = "text"
            Post.objects.create(
                  title=title,
                  text=text,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.video_url:
            title = new.title
            video = new.video_url
            author = author
            block = block
            post_type = "video"
            Post.objects.create(
                  title=title,
                  video=video,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         else:
            pass

@receiver(post_save, sender=Post)
def post_save_create_estate_post(sender, created, instance, **kwargs):    
   api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
   query = "Real estate"
   username = "pyramid"
   pk = 3
   news = api.news_api(q=query, language="en")
   block = get_object_or_404(Block, id=pk)
   author = get_object_or_404(User, username=username)
   if created:
      for new in news.results():
         if new.image_url:
            title = new.title
            attachment = new.image_url
            author = author
            block = block
            post_type = "image"
            Post.objects.create(
                  title=title,
                  attachment=attachment,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.link:
            title = new.title
            link = new.link
            author = author
            block = block
            post_type = "link"
            Post.objects.create(
                  title=title,
                  link=link,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.content:
            title = new.title
            text = new.content
            author = author
            block = block
            post_type = "text"
            Post.objects.create(
                  title=title,
                  text=text,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.video_url:
            title = new.title
            video = new.video_url
            author = author
            block = block
            post_type = "video"
            Post.objects.create(
                  title=title,
                  video=video,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         else:
            pass

@receiver(post_save, sender=Post)
def post_save_create_forex_post(sender, created, instance, **kwargs):    
   api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
   query = "Forex"
   username = "leox"
   pk = 5
   news = api.news_api(q=query, language="en")
   block = get_object_or_404(Block, id=pk)
   author = get_object_or_404(User, username=username)
   if created:
      for new in news.results():
         if new.image_url:
            title = new.title
            attachment = new.image_url
            author = author
            block = block
            post_type = "image"
            Post.objects.create(
                  title=title,
                  attachment=attachment,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.link:
            title = new.title
            link = new.link
            author = author
            block = block
            post_type = "link"
            Post.objects.create(
                  title=title,
                  link=link,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.content:
            title = new.title
            text = new.content
            author = author
            block = block
            post_type = "text"
            Post.objects.create(
                  title=title,
                  text=text,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.video_url:
            title = new.title
            video = new.video_url
            author = author
            block = block
            post_type = "video"
            Post.objects.create(
                  title=title,
                  video=video,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         else:
            pass

@receiver(post_save, sender=Post)
def post_save_create_economy_post(sender, created, instance, **kwargs):    
   api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
   query = "Economy"
   username = "pyramid"
   pk = 6
   news = api.news_api(q=query, language="en")
   block = get_object_or_404(Block, id=pk)
   author = get_object_or_404(User, username=username)
   if created:
      for new in news.results():
         if new.image_url:
            title = new.title
            attachment = new.image_url
            author = author
            block = block
            post_type = "image"
            Post.objects.create(
                  title=title,
                  attachment=attachment,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.link:
            title = new.title
            link = new.link
            author = author
            block = block
            post_type = "link"
            Post.objects.create(
                  title=title,
                  link=link,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.content:
            title = new.title
            text = new.content
            author = author
            block = block
            post_type = "text"
            Post.objects.create(
                  title=title,
                  text=text,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         elif new.video_url:
            title = new.title
            video = new.video_url
            author = author
            block = block
            post_type = "video"
            Post.objects.create(
                  title=title,
                  video=video,
                  author=author,
                  block=block,
                  post_type=post_type,
               )
         else:
            pass
