import jwt
import os
import requests
import random
import string
import re
import finnhub
import time
import json
from decouple import config
from requests_oauthlib import OAuth1
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponsePermanentRedirect, JsonResponse, HttpResponse
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
from django.utils import timezone
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from newsdataapi import NewsDataApiClient

from utils.utils import Util
from core.models import User
from block.models import Post, Block
from block.api.serializers import BlockSerializer, PostSerializer_detailed, BlockDetailSerializer
from core.api.serializers import ListUserSerializer, UserProfileSerializer

from rest_framework import generics, status, views, permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

# SPOTLIGHT
"""
class SearchTopBlocks(ListAPIView):  # TODO Look for a better method to search top blocks
    
    Returns top blocks which matches users search.
    

    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get(self, request):
        block = Block.objects.filter(is_deleted=False).order_by("-subscriber_count")
        serializer = self.serializer_class(block, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SearchTopPosts(ListAPIView):
    
    Returns all top posts.
    

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = SearchFilter
    search_fields = (
        "^title",
        "^block__name",
        "^author__name",
        "^author__username",
        "text",
    )

    def get(self, request):
        post = Post.objects.filter(is_deleted=False).order_by("-votes")
        serializer = self.serializer_class(post, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SearchTopUsers(ListAPIView):  # TODO Makeit proper
    
    Returns all users.

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = ListUserSerializer
    filter_backends = SearchFilter
    search_fields = ("username", "name", "bio") 
"""

# LATEST
class SearchLatest(ListAPIView):
    """
    Returns all latest posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer_detailed
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter,)
    search_fields = ("title", "block__name", "author__name", "author__username")


# PEOPLE
class SearchUsers(ListAPIView):
    """
    Returns all users.
    """
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter,)
    search_fields = ("username", "name", "bio")


# PEOPLE
class FeaturedUsers(ListAPIView):
    """
    Returns all 3 latest users.
    """
    queryset = User.objects.all()[:5]
    serializer_class = ListUserSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter,)
    search_fields = ("username", "name", "bio")



# PEOPLE
class RecommendedUsers(ListAPIView):
    """
    Returns all 10 latest users.
    """
    queryset = User.objects.all()[:10]
    serializer_class = ListUserSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter,)
    search_fields = ("username", "name", "bio")


# BLOCKS
class FeaturedBlocks(ListAPIView):
    """
    Returns all 6 latest blocks.
    """
    queryset = Block.objects.all()[:6]
    serializer_class = BlockDetailSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter,)
    search_fields = ("name", "desc", "about", "category")


class SearchBlocks(ListAPIView):
    """
    Returns all blocks.
    """
    queryset = Block.objects.all()
    serializer_class = BlockDetailSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter,)
    search_fields = ("name", "desc", "about", "category")


class BlockCategory(ListAPIView):
    """
    Returns all blocks that has been created by their category.
    """
    queryset = Block.objects.all()
    serializer_class = BlockDetailSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


# POSTS
class SearchPosts(ListAPIView):
    """
    Returns all posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer_detailed
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter,)
    search_fields = ("title", "block__name", "author__name", "author__username")


# TODO Build Recommendation Algorithms (Next Year)
class ListAllPosts(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer_detailed
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination    
    filter_backends = (SearchFilter,)
    search_fields = ("title", "block__name", "author__name", "author__username")


# CRYPTO
class GetCryptoPriceData(GenericAPIView):
    permission_classes = (AllowAny,)

    # Get this crypto symbols to use in the frontend  BINANCE:BTCUSDT, BINANCE:ETHUSDT, BINANCE:XRPUSDT, BINANCE:DOGEUSDT, BINANCE:SHIBUSDT, BINANCE:BNBUSDT, BINANCE:ADAUSDT, BINANCE:MATICUSDT, BINANCE:DOTUSDT, BINANCE:TRXUSDT
    def post(self, request):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(
            api_key="ce62842ad3ien0nq88c0ce62842ad3ien0nq88cg"
        )

        time = request.data.get("timeframe")
        sym = request.data.get("symbol")

        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)
        one_day_ago = current_time - timedelta(hours=24)
        week_ago = current_time - timedelta(days=7)
        month_ago = current_time - timedelta(days=31)
        year_ago = current_time - timedelta(weeks=51)
        current_time_unix = datetime.timestamp(current_time) * 1000
        one_hour_ago_unix = datetime.timestamp(one_hour_ago) * 1000
        one_day_ago_unix = datetime.timestamp(one_day_ago) * 1000
        week_ago_unix = datetime.timestamp(week_ago) * 1000
        month_ago_unix = datetime.timestamp(month_ago) * 1000
        year_ago_unix = datetime.timestamp(year_ago) * 1000

        # time is simply the historical data of an asset sent to the request_params (i.e 1D, 1W, 1M, 3M, 1Y, 5Y)
        if time == "1Y":
            crypto_data = finnhub_client.crypto_candles(
                sym, 5, 1651359600, 1667257200
            )  # 2488320 datapoints recieved
        elif time == "1M":
            crypto_data = finnhub_client.crypto_candles(
                sym, 5, 1667257200, 1669849200
            )  # 207360 datapoints recieved
        elif time == "1W":
            crypto_data = finnhub_client.crypto_candles(
                sym, 5, 1670713200, 1671231600
            )  # 16128 datapoints recieved
        elif time == "1D":
            crypto_data = finnhub_client.crypto_candles(
                sym, 1, 1671360433, 1671446833
            )  # 1440 datapoints redieved
        else:
            crypto_data = finnhub_client.crypto_candles(
                sym, 1, 1671447600, 1671451200
            )  # 60 datapoints redieved

        return Response(
            {
                "data": crypto_data,
            },
            status=status.HTTP_200_OK,
        )


class GetCryptoProfileBySymbol(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        specific = request.data.get("symbol")

        profile = finnhub_client.crypto_profile(specific)
        return Response(
            {
                "data": profile,
            },
            status=status.HTTP_200_OK,
        )

# STOCKS
class GetStockPriceData(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(
            api_key="ce62842ad3ien0nq88c0ce62842ad3ien0nq88cg"
        )

        time = request.data.get("timeframe")
        sym = request.data.get("symbol")

        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)
        one_day_ago = current_time - timedelta(hours=24)
        week_ago = current_time - timedelta(days=7)
        month_ago = current_time - timedelta(days=31)
        year_ago = current_time - timedelta(weeks=51)
        current_time_unix = datetime.timestamp(current_time) * 1000
        one_hour_ago_unix = datetime.timestamp(one_hour_ago) * 1000
        one_day_ago_unix = datetime.timestamp(one_day_ago) * 1000
        week_ago_unix = datetime.timestamp(week_ago) * 1000
        month_ago_unix = datetime.timestamp(month_ago) * 1000
        year_ago_unix = datetime.timestamp(year_ago) * 1000

        # time is simply the historical data of an asset sent to the request_params (i.e 1H, 1D, 1W, 1M,  1Y)
        if time == "1Y":
            stock_data = finnhub_client.stock_candles(
                sym, 5, 1651359600, 1667257200
            )  # 2488320 datapoints recieved
        elif time == "1M":
            stock_data = finnhub_client.stock_candles(
                sym, 5, 1667257200, 1669849200
            )  # 207360 datapoints recieved
        elif time == "1W":
            stock_data = finnhub_client.stock_candles(
                sym, 5, 1670713200, 1671231600
            )  # 16128 datapoints recieved
        elif time == "1D":
            stock_data = finnhub_client.stock_candles(
                sym, 1, 1671360433, 1671446833
            )  # 1440 datapoints redieved
        else:
            stock_data = finnhub_client.stock_candles(
                sym, 1, 1671447600, 1671451200
            )  # 60 datapoints redieved

        return Response(
            {
                "data": stock_data,
            },
            status=status.HTTP_200_OK,
        )


class GetCompanyFinancials(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        specific = request.data.get("company")

        financials = finnhub_client.company_basic_financials(specific, "all")
        return Response(
            {
                "data": financials,
            },
            status=status.HTTP_200_OK,
        )


class GetCompanyProfile(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        specific = request.data.get("company")

        profile = finnhub_client.company_profile(symbol=specific)
        return Response(
            {
                "data": profile,
            },
            status=status.HTTP_200_OK,
        )


class SearchStocks(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, text):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        specific = text

        search = finnhub_client.symbol_lookup(specific)
        return Response(
            {
                "data": search,
            },
            status=status.HTTP_200_OK,
        )


class GetCompanySecondProfile(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        specific = request.data.get("company")

        profile = finnhub_client.company_profile2(symbol=specific)
        return Response(
            {
                "data": profile,
            },
            status=status.HTTP_200_OK,
        )


class GetStockQuoteData(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        specific = request.data.get("symbol")

        quote = finnhub_client.quote(specific)
        return Response(
            {
                "data": quote,
            },
            status=status.HTTP_200_OK,
        )


class GetStocksByThemes(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        FINNHUB_API_KEY = config("FINNHUB_API_KEY")
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        specific = request.data.get("theme")

        theme = finnhub_client.stock_investment_theme(specific)
        return Response(
            {
                "data": theme,
            },
            status=status.HTTP_200_OK,
        )


# NEWS


class GetCryptoNews(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        NEWSDATA_API_KEY = config("NEWSDATA_API_KEY")
        api = NewsDataApiClient(apikey="pub_1612976c905083433c26d4ac689267103ccfb")
        specific = request.data.get("crypto")

        news = api.crypto_api(q=specific, language="en")
        return Response(
            {
                "data": news,
            },
            status=status.HTTP_200_OK,
        )


class GetStockNews(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        NEWSDATA_API_KEY = config("NEWSDATA_API_KEY")
        api = NewsDataApiClient(apikey="pub_1612976c905083433c26d4ac689267103ccfb")
        specific = request.data.get("stock")

        news = api.news_api(q=specific, language="en")
        return Response(
            {
                "data": news,
            },
            status=status.HTTP_200_OK,
        )


class GetCategoryNews(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(
        self, request, category
    ):  # can bt one of the following stocks, crypto, currencies, arts, real estate,wold economy, pub_1524778c92e3df5c784193332a4a5fba4158c
        api = NewsDataApiClient(apikey="pub_14763965a946ce477ec7b9d12746e1e0c5adf")
        specific = category

        news = api.news_api(q=specific, language="en")
        return Response(
            {
                "data": news,
            },
            status=status.HTTP_200_OK,
        )

    
class GetBusinessNews(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(
        self, request
    ):  # can bt one of the following stocks, crypto, currencies, arts, real estate,wold economy,
        NEWSDATA_API_KEY = config("NEWSDATA_API_KEY")
        api = NewsDataApiClient(apikey="pub_1612976c905083433c26d4ac689267103ccfb")

        news = api.news_api(category="business", language="en")
        return Response(
            {
                "data": news,
            },
            status=status.HTTP_200_OK,
        )    