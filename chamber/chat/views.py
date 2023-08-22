import jwt
import os
import requests
import random
import string
import re
from datetime import datetime, timedelta
 
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views import View
from django.views.generic import *
from django.db.models import Count

from .serializers import *
from .models import *
from core.models import User
from utils.pagination import CustomPagination
from notifications.models import Notification

from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)



class CreateChamberView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChamberSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")
        cover = request.data.get("cover")
        room_name = request.data.get("room_name")
        about = request.data.get("about")
        chamber_type = request.data.get("chamber_type")
        category = request.data.get("category")
        username = request.data.get("username")
        creator = get_object_or_404(User, username=username)

        with transaction.atomic():
            chamber = Chamber.objects.create(
                creator=creator, 
                room_name=room_name, 
                chamber_type=chamber_type, 
                category=category, 
                avatar=avatar, 
                cover=cover, 
                about=about
            )
        d = ChamberSerializer(chamber).data
        return Response(d, status=status.HTTP_201_CREATED)


class ChamberDetailView(RetrieveAPIView):
    lookup_field = "room_name"
    permission_classes = (AllowAny,)
    serializer_class = ChamberSerializer
    queryset = Chamber.objects.all()


class ChamberUpdateView(UpdateAPIView):
    lookup_field = "room_name"
    permission_classes = (AllowAny,)
    serializer_class = ChamberSerializer
    queryset = Chamber.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class ChamberDeleteView(DestroyAPIView):
    lookup_field = "room_name"
    permission_classes = (AllowAny,)
    serializer_class = ChamberSerializer
    queryset = Chamber.objects.all()


class ListChambersOfUsers(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChamberSerializer
    queryset = Chamber.objects.all()

    def get(self, request):
        chamber = Chamber.objects.filter(creator=self.request.user)
        serializer = ChamberSerializer(chamber, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_creator_chamber(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        chamber = get_object_or_404(Chamber, id=pk)
        if request.user is chamber.creator:
            creator = True
        else:
            creator = False
        return Response(
            {
                "creator": creator,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_joined_chamber(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        chamber = get_object_or_404(Chamber, id=pk)
        if request.user in chamber.subscribed_users.all():
            joined = True
        else:
            joined = False
        return Response(
            {
                "joined": joined,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def join_chamber(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        chamber = get_object_or_404(Chamber, id=pk)
        if request.user in chamber.subscribed_users.all():
            joined = False
            chamber.subscribed_users.remove(request.user)
            chamber.subscriber_count = chamber.subscriber_count - 1
            chamber.save()
        else:
            joined = True
            chamber.subscribed_users.add(request.user)
            chamber.subscriber_count = chamber.subscriber_count + 1
            chamber.save()
        return Response(
            {
                "joined": joined,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_blocked_in_chamber(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        chamber = get_object_or_404(Chamber, id=pk)
        if request.user in chamber.blocked_users.all():
            blocked = True
        else:
            blocked = False
        return Response(
            {
                "blocked": blocked,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def block_user_in_chamber(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        chamber = get_object_or_404(Chamber, id=pk)
        if request.user in chamber.blocked_users.all():
            blocked = False
            chamber.blocked_users.remove(request.user)
            chamber.save()
        else:
            blocked = True
            chamber.blocked_users.add(request.user)
            chamber.save()
        return Response(
            {
                "blocked": blocked,
            },
            status=status.HTTP_201_CREATED,
        )


class CreateBotView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BotSerializer

    def create(self, request, *args, **kwargs):
        file_name = request.data.get("file_name")
        message_handler = request.data.get("message_handler")
        description = request.data.get("description")
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)

        with transaction.atomic():
            bot = Bot.objects.create(
                user=user, 
                file_name=file_name, 
                message_handler=message_handler, 
                description=description
            )
        d = BotSerializer(bot).data
        return Response(d, status=status.HTTP_201_CREATED)


class BotDetailView(RetrieveAPIView):
    lookup_field = "file_name"
    permission_classes = (AllowAny,)
    serializer_class = BotSerializer
    queryset = Bot.objects.all()


class BotUpdateView(UpdateAPIView):
    lookup_field = "file_name"
    permission_classes = (AllowAny,)
    serializer_class = BotSerializer
    queryset = Bot.objects.all()


class BotDeleteView(DestroyAPIView):
    lookup_field = "file_name"
    permission_classes = (AllowAny,)
    serializer_class = BotSerializer
    queryset = Bot.objects.all()


@api_view(['GET'])
def getMe(request):
    ip_addr = request.META.get('HTTP_X_FORWADED_FOR') or request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')

    return Response(
        {
            'ip_address':ip_addr,
            'user_agent':user_agent
        }
    )


@api_view(['GET'])
@permission_classes((AllowAny,))
def ListChatsOfChamber(request, id):
    chamber_chats = Chat.objects.filter(room__id=id)
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(chamber_chats,request)

    serializer = ChamberSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response({'data':serializer.data})    


class ChatDeleteView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        data = request.data
        chat = get_object_or_404(Chat,id=data.get('chat_id'))
        if chat.from_user == request.user:
            chat.delete()
            return Response({"chat_deleted": True})
        return Response({"chat_deleted": False})

