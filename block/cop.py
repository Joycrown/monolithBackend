import datetime
from newsdataapi import NewsDataApiClient
from django.shortcuts import get_object_or_404

from block.models import *
from core.models import User



def finance_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Finance"
      username = "pyramid"
      pk = 6
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[1]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[1]['title'],
                     attachment=value[1]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  )
            if value[2]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[2]['title'],
                     video=value[2]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[5]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[5]['title'],
                     attachment=value[5]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  ) 
            if value[6]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[6]['title'],
                     video=value[6]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[8]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[8]['title'],
                     video=value[8]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass     


def crypto_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Cryptocurrency"
      username = "lumba"
      pk = 2
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[1]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[1]['title'],
                     attachment=value[1]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  )
            if value[2]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[2]['title'],
                     video=value[2]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[5]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[5]['title'],
                     attachment=value[5]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  ) 
            if value[6]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[6]['title'],
                     video=value[6]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[8]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[8]['title'],
                     video=value[8]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass


def stock_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Stocks"
      username = "roland"
      pk = 3
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[1]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[1]['title'],
                     attachment=value[1]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  )
            if value[2]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[2]['title'],
                     video=value[2]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[5]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[5]['title'],
                     attachment=value[5]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  ) 
            if value[6]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[6]['title'],
                     video=value[6]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[8]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[8]['title'],
                     video=value[8]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass


def real_estate_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Real estate"
      username = "benlo"
      pk = 1
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[1]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[1]['title'],
                     attachment=value[1]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  )
            if value[2]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[2]['title'],
                     video=value[2]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[5]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[5]['title'],
                     attachment=value[5]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  ) 
            if value[6]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[6]['title'],
                     video=value[6]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[8]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[8]['title'],
                     video=value[8]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass


def forex_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "Forex"
      username = "pyramid"
      pk = 5
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[1]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[1]['title'],
                     attachment=value[1]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  )
            if value[2]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[2]['title'],
                     video=value[2]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[5]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[5]['title'],
                     attachment=value[5]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  ) 
            if value[6]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[6]['title'],
                     video=value[6]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[8]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[8]['title'],
                     video=value[8]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass


def economy_post():
      api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
      query = "World Economy"
      username = "benlo"
      pk = 6
      news = api.news_api(q=query, language="en")
      block = get_object_or_404(Block, id=pk)
      author = get_object_or_404(User, username=username)
      for key, value in news.items():
         if key == 'results':
            if value[0]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[0]['title'],
                     text=value[0]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )
            if value[1]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[1]['title'],
                     attachment=value[1]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  )
            if value[2]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[2]['title'],
                     video=value[2]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[3]['link'] != None: #Create link post
               Post.objects.create(
                     title=value[3]['title'],
                     link=value[3]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )                          
            if value[4]['content'] != None: #Create text post
               Post.objects.create(
                     title=value[4]['title'],
                     text=value[4]['content'],
                     author=author,
                     block=block,
                     post_type="text",
                  )                
            if value[5]['image_url'] != None: #Create image post
               Post.objects.create(
                     title=value[5]['title'],
                     attachment=value[5]['image_url'],
                     author=author,
                     block=block,
                     post_type="image",
                  ) 
            if value[6]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[6]['title'],
                     video=value[6]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[7]['link'] != None: #Create link post 
               Post.objects.create(
                     title=value[7]['title'],
                     link=value[7]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
            if value[8]['video_url'] != None: #Create video post 
               Post.objects.create(
                     title=value[8]['title'],
                     video=value[8]['video_url'],
                     author=author,
                     block=block,
                     post_type="video",
                  )
            if value[9]['link'] != None: #Create link post       
               Post.objects.create(
                     title=value[9]['title'],
                     link=value[9]['link'],
                     author=author,
                     block=block,
                     post_type="link",
                  )
         else: 
            pass
