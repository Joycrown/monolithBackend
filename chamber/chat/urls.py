from django.urls import path

from . import views

urlpatterns = [
    path('create-chamber', views.CreateChamberView, name='create-chamber'),
    path('chamber-detail/<str:room_name>', views.ChamberDetailView, name='chamber-detail'),
    path('chamber-update/<str:room_name>', views.ChamberUpdateView, name='chamber-update'),
    path('chamber-delete/<str:room_name>', views.ChamberDeleteView, name='chamber-delete'),
    path('list-users-chambers', views.ListChambersOfUsers, name='list-users-chambers'),
    path('u/creator/chamber', views.user_creator_chamber, name='user_creator_chamber'),
    path('u/joined/chamber', views.user_joined_chamber, name='user_joined_chamber'),
    path('join/chamber', views.join_chamber, name='join_chamber'),
    path('u/blocked/in/chamber', views.user_blocked_in_chamber, name='user_blocked_in_chamber'),
    path('block/user/in/chamber', views.block_user_in_chamber, name='block_user_in_chamber'),
    path('create-bot', views.CreateBotView, name='create-bot'),
    path('bot-detail/<str:room_name>', views.BotDetailView, name='bot-detail'),
    path('bot-update/<str:room_name>', views.BotUpdateView, name='bot-update'),
    path('bot-delete/<str:room_name>', views.BotDeleteView, name='bot-delete'),
    path('getMe', views.getMe, name='get_me'),
    path('list_chambers_chats/<int:id>', views.ListChatsOfChamber, name='list_chambers_chats'),
    path('chat-delete', views.ChatDeleteView, name='chat-delete')
]
