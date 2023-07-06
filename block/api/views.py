import jwt
import os
import requests
import random
import string
import re
 
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
from block.models import *
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
from rest_framework.renderers import JSONRenderer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)

# TODO Notifications automatically from the block you are part of, on comments on your posts


class CreateBlockView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BlockDetailSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        avatar = request.data.get("avatar")
        cover = request.data.get("cover")
        name = request.data.get("name")
        desc = request.data.get("desc")
        about = request.data.get("about")
        block_type = request.data.get("block_type")
        category = request.data.get("category")
        username = request.data.get("username")
        creator = get_object_or_404(User, username=username)

        with transaction.atomic():
            block = Block.objects.create(
                creator=creator, name=name, block_type=block_type, category=category, avatar=avatar, cover=cover, desc=desc, about=about
            )
        d = BlockDetailSerializer(block).data
        return Response(d, status=status.HTTP_201_CREATED)


class BlockDetailView(RetrieveAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = BlockDetailSerializer
    queryset = Block.objects.all()


class BlockUpdateView(UpdateAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = BlockDetailSerializer
    queryset = Block.objects.all()
    parser_classes = (FormParser, MultiPartParser)


class BlockDeleteView(DestroyAPIView):
    lookup_field = "name"
    permission_classes = (AllowAny,)
    serializer_class = BlockSerializer
    queryset = Block.objects.all()


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_creator_block(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        block = get_object_or_404(Block, id=pk)
        if request.user is block.creator:
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
def user_joined_block(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        block = get_object_or_404(Block, id=pk)
        if request.user in block.subscribers.all():
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
def join_block(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        block = get_object_or_404(Block, id=pk)
        if request.user in block.subscribers.all():
            joined = False
            block.subscribers.remove(request.user)
            block.subscriber_count = block.subscriber_count - 1
            block.save()
        else:
            joined = True
            block.subscribers.add(request.user)
            block.subscriber_count = block.subscriber_count + 1
            block.save()
        return Response(
            {
                "joined": joined,
            },
            status=status.HTTP_201_CREATED,
        )


class ListBlocksUserJoined(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = BlockSerializer

    def get(self, request, username):
        # blocks = Block.objects.all()
        user = get_object_or_404(User, username=username)
        block = user.subscribers.all()

        if block > 0:
            serializer = self.serializer_class(block, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "there are no blocks user joined"},
                status=status.HTTP_200_OK,
            )

        # for block in blocks:
        #     if user in block.subscribers.all():
        #         serializer = self.serializer_class(block, many=True)
        #         return Response(data=serializer.data, status=status.HTTP_200_OK)
        #     else:
        #         return Response(
        #             {"message": "there are no blocks user joined"},
        #             status=status.HTTP_200_OK,
        #         )


class ListLinksOfBlock(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def get(self, request, name):
        # link = get_object_or_404(Link, block__name=name)
        link = Link.objects.filter(block__name=name)
        serializer = LinkSerializer(link, many=True)
        return Response(serializer.data)


class CreateLinkView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = LinkSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        title = request.data.get("title")
        image = request.data.get("image")
        url = request.data.get("url")
        block = Block.objects.get(name=name)

        with transaction.atomic():
            link = Link.objects.create(block=block, image=image, title=title, url=url)
        d = LinkSerializer(link).data
        return Response(d, status=status.HTTP_201_CREATED)


class LinkDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (AllowAny,)
    serializer_class = LinkSerializer
    queryset = Link.objects.all()


class ListRulesOfBlock(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()

    def list(self, request, name):
        # rule = get_object_or_404(Rule, block__name=name)
        rule = Rule.objects.filter(block__name=name)
        serializer = RuleSerializer(rule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateRuleView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = RuleSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        title = request.data.get("title")
        text = request.data.get("text")
        block = Block.objects.get(name=name)

        with transaction.atomic():
            rule = Rule.objects.create(block=block, text=text, title=title)
        d = RuleSerializer(rule).data
        return Response(d, status=status.HTTP_201_CREATED)


class RuleDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (AllowAny,)
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()


class ListBlocksOfUser(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = BlockSerializer

    def get(self, request, username):
        block = Block.objects.filter(creator__username=username)
        serializer = self.serializer_class(block, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListBlocksUserIsModerator(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = BlockSerializer

    def get(self, request, username):
        blocks = Block.objects.all()
        user = get_object_or_404(User, username=username)
        for block in blocks:
            if user in block.moderators.all():
                serializer = self.serializer_class(block, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"there are no blocks user is moderator of"},
                    status=status.HTTP_200_OK,
                )


@api_view(["POST"])
@permission_classes((AllowAny,))
def RePostView(request):
    title = request.data.get("title")
    p_id = request.data.get("p_id")
    b_id = request.data.get("b_id")

    try:
        post = get_object_or_404(Post, id=p_id)
        block = get_object_or_404(Block, id=b_id)
    except:
        raise exceptions.APIException("Not Found ! ")
    if post.author == request.user:
        raise exceptions.APIException("Can't Repost your own post")
    # try:
    parent_post = Post.objects.filter(parent=post, author=request.user)
    if parent_post.exists():
        raise exceptions.APIException("Already reposted !")
    else:
        with transaction.atomic():
            re_post = Post.objects.create(
                title=title,
                block=block,
                author=request.user,
                parent=post,
                is_repost=True,
            )
            post.reposts = post.reposts + 1
            post.save()
            Notification.objects.get_or_create(
                notification_type="RP",
                post=re_post,
                comments=(
                    f"@{request.user.username} reposted your post in {block.name}"
                ),
                to_user=post.author,
                from_user=request.user,
            )
        serializer = PostSerializer(re_post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreatePostView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        pk = request.data.get("pk")
        attachment = request.data.get("attachment")
        video = request.data.get("video")
        link = request.data.get("link")
        text = request.data.get("text")
        post_type = request.data.get("post_type")
        block = get_object_or_404(Block, id=pk)
        author = request.user

        with transaction.atomic():
            post = Post.objects.create(
                title=title,
                attachment=attachment,
                video=video,
                link=link,
                text=text,
                author=author,
                block=block,
                post_type=post_type,
            )
        d = PostSerializer(post).data
        return Response(d, status=status.HTTP_201_CREATED)


class PostCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        title = request.data.get("title")
        pk = request.data.get("pk")
        attachment = request.data.get("attachment")
        username = request.data.get("username")
        video = request.data.get("video")
        link = request.data.get("link")
        text = request.data.get("text")
        post_type = request.data.get("post_type")
        block = get_object_or_404(Block, id=pk)
        author = get_object_or_404(User, username=username)

        with transaction.atomic():
            post = Post.objects.create(
                title=title,
                attachment=attachment,
                video=video,
                link=link,
                text=text,
                author=author,
                block=block,
                post_type=post_type,
            )
        d = PostSerializer(post).data
        return Response(d, status=status.HTTP_201_CREATED)


class PostDeleteView(APIView):
    permission_classes = (AllowAny, )

    def post(self,request):
        data = request.data
        post = get_object_or_404(Post,id=data.get('post_id'))
        if post.author == request.user:
            post.delete()
            return Response({"post_deleted": True})


class PostUpdateView(UpdateAPIView):
    lookup_field = "id"
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (FormParser, MultiPartParser)

#class ListPostsOfUser(ListAPIView):
#    queryset = Post.objects.all()
#    permission_classes = (AllowAny,)
 #   pagination_class = CustomPagination
  #  serializer_class = PostSerializer_detailed
#
 #   def get(self, request, username, *args, **kwargs):
  #      paginator = CustomPagination()
  #      post = Post.objects.filter(
    #        author__username=username, is_reviewed=True, is_deleted=False
   #     )
    #    result_page = paginator.paginate_queryset(post)
    #    serializer = self.get_serializer(result_page, many=True)
     #   return paginator.get_paginated_response({'data':serializer.data, 'noti_count': noti_count})


class PostDeleteView(DestroyAPIView):
    lookup_field = "id"
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


@api_view(['GET'])
@permission_classes((AllowAny,))
def ListPostsOfUser(request, username):
    post = Post.objects.filter(
            author__username=username, is_reviewed=True, is_deleted=False
        )
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(post,request)

    serializer = PostSerializer_detailed(result_page, many=True, context={
                                        
                                        'request': request
                                        })
    return paginator.get_paginated_response({'data':serializer.data})    
    

class DetailPostOfUser(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer_detailed
        return PostSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "author__username": self.kwargs["username"],
            "id": self.kwargs["p_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


#class ListPostsOfBlock(ListAPIView):
 #   queryset = Post.objects.all()
  #  permission_classes = (AllowAny,)
 #   pagination_class = CustomPagination
  #  serializer_class = PostSerializer_detailed
#
 #   def get(self, request, b_name, *args, **kwargs):
  #      post = Post.objects.filter(
  #          block__name=b_name, is_reviewed=True, is_deleted=False
   #     )
   #     paginatedResult = self.paginate_queryset(post)
   #     serializer = self.get_serializer(paginatedResult, many=True)
    #    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
def ListPostsOfBlock(request, b_name):
    post = Post.objects.filter(
            block__name=b_name, is_reviewed=True, is_deleted=False
        )
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(post,request)

    serializer = PostSerializer_detailed(result_page, many=True, context={
                                        
                                        'request': request
                                        })
    return paginator.get_paginated_response({'data':serializer.data})     
    

class DetailPostOfBlock(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostSerializer_detailed
        return PostSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {"block__name": self.kwargs["b_name"], "id": self.kwargs["p_id"]}
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class ListSavedPostsOfUser(ListAPIView):
    queryset = Post.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = PostSerializer_detailed

    def get(self, request):
        posts = Post.objects.filter(is_reviewed=True, is_deleted=False).order_by(
            "-created"
        )
        for post in posts:
            if self.request.user in post.saved.all():
                serializer = self.serializer_class(posts, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"there are no saved posts from user"}, status=status.HTTP_200_OK
                )


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_saved_post(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if request.user in post.saved.all():
            saved = True
        else:
            saved = False
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def save_post(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if request.user in post.saved.all():
            saved = False
            post.saved.remove(request.user)
            post.saved_count = post.saved_count - 1
            post.save()
        else:
            saved = True
            post.saved.add(request.user)
            post.saved_count = post.saved_count + 1
            post.save()
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_reported_post(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if request.user in post.report.all():
            report = True
        else:
            report = False
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def report_post(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if request.user in post.report.all():
            report = False
            post.report.remove(request.user)
            post.report_count = post.report_count - 1
            post.save()
        else:
            report = True
            post.report.add(request.user)
            post.report_count = post.report_count + 1
            post.save()
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def VoteOnPost(request):
    if request.method == "POST":
        voter = request.user
        post_id = request.data.get("post_id")
        value = request.data.get("value")
        post = get_object_or_404(Post, id=post_id)

        if value == 1:
            Notification.objects.get_or_create(
                notification_type="VP",
                post=post,
                comments=(
                    f"Go see your post on {post.block.name}: “{post.title}...”"
                ),
                to_user=post.author,
                from_user=voter,
            )
        try:
            vote = Vote.objects.get(voter=voter, post=post)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voter, value, post=post)
        else:
            if value in [-1, 1]:
                vote.value = value
                vote.save()
            elif value == 0:
                vote.delete()

        return Response(
            {"post": PostSerializer(get_object_or_404(Post, id=post_id)).data},
                status=status.HTTP_201_CREATED,
        )        
        
        

class RetrievePost(ListAPIView):
    queryset = Post.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = self.serializer_class(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_voted_post(request):
    if request.method == "POST":
        voter = request.user
        pk = request.data.get("pk")
        post = get_object_or_404(Post, id=pk)
        if voter in post.voters.all():
            voted = True
            vote = Vote.objects.get(voter=voter, post=post).value
        else:
            voted = False
            vote = 0
        return Response(
            {
                "voted": voted,
                "vote": vote,
            },
            status=status.HTTP_200_OK,
        )


class CreateCommentView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        author = request.user
        post_id = request.data.get("post_id")
        text = request.data.get("text")
        parent_comment_id = request.data.get("parent_comment_id")
        post = get_object_or_404(Post, id=post_id)

        with transaction.atomic():
            comment = Comment.objects.create(
                post=post,
                author=author,
                parent_comment=parent_comment_id
                and Comment.objects.get(pk=parent_comment_id),
                text=text,
            )
            post.comments = post.comments + 1
            post.save()
        if parent_comment_id and Comment.objects.get(pk=parent_comment_id):
            Notification.objects.get_or_create(
                notification_type="C",
                comment=Comment.objects.get(pk=parent_comment_id),
                comments=(
                    f"@{author.username} replied to your comment in b/{post.block.name}"
                ),
                to_user=Comment.objects.get(pk=parent_comment_id).author,
                from_user=author,
            )
        else:
            Notification.objects.get_or_create(
                notification_type="P",
                post=post,
                comments=(
                    f"@{author.username} replied to your post in b/{post.block.name}"
                ),
                to_user=post.author,
                from_user=author,
            )

        d = CommentSerializer(comment).data
        return Response(d, status=status.HTTP_201_CREATED)


    
@api_view(["POST"])
@permission_classes((AllowAny,))
def VoteOnComment(request):
    if request.method == "POST":
        voter = request.user
        comment_id = request.data.get("comment_id")
        value = request.data.get("value")
        comment = get_object_or_404(Comment, id=comment_id)

        if value == 1:
            Notification.objects.get_or_create(
                notification_type="VC",
                comment=comment,
                comments=(
                    f"Go see your comment on {comment.post.block.name}: “{comment.post.title}...”"
                ),
                to_user=comment.author,
                from_user=voter,
            )
        try:
            vote = Vote.objects.get(voter=voter, comment=comment)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voter, value, comment=comment)
        else:
            if value in [-1, 1]:
                vote.value = value
                vote.save()
            elif value == 0:
                vote.delete()

        return Response(
            {
                "comment": CommentSerializer(
                    get_object_or_404(Comment, id=comment_id)
                ).data
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_voted_comment(request):
    if request.method == "POST":
        voter = request.user
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if voter in comment.voters.all():
            voted = True
            vote = Vote.objects.get(voter=voter, comment=comment).value
        else:
            voted = False
            vote = 0
        return Response(
            {
                "voted": voted,
                "vote": vote,
            },
            status=status.HTTP_200_OK,
        )


class ListSavedCommentsOfUser(ListAPIView):
    queryset = Comment.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer_detailed

    def get(self, request):
        comments = Comment.objects.filter(is_deleted=False).order_by("-created")
        for comment in comments:
            if self.request.user in comment.saved.all():
                serializer = self.serializer_class(comments, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"there are no saved comments from user"}, status=status.HTTP_200_OK
                )


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_saved_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.saved.all():
            saved = True
        else:
            saved = False
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_reported_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.report.all():
            report = True
        else:
            report = False
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def save_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.saved.all():
            saved = False
            comment.saved.remove(request.user)
        else:
            saved = True
            comment.saved.add(request.user)
        return Response(
            {
                "saved": saved,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes((AllowAny,))
def report_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.report.all():
            report = False
            comment.report.remove(request.user)
        else:
            report = True
            comment.report.add(request.user)
        return Response(
            {
                "report": report,
            },
            status=status.HTTP_201_CREATED,
        )


class ListNewCommentsOfPost(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__block__name=self.kwargs["b_name"], post__id=self.kwargs["p_id"]
        ).order_by("-created")


class ListOldCommentsOfPost(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__block__name=self.kwargs["b_name"], post__id=self.kwargs["p_id"]
        ).order_by("created")


class ListPopularCommentsOfPost(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            post__block__name=self.kwargs["b_name"], post__id=self.kwargs["p_id"]
        ).order_by("votes")


class DetailCommentsOfPost(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        return CommentSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "post__block__name": self.kwargs["b_name"],
            "post__id": self.kwargs["p_id"],
            "id": self.kwargs["c_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class ListCommentsOfUser(ListCreateAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        if self.request.method == "POST":
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            author__username=self.kwargs["username"]
        ).order_by("-created")


class DetailCommentsOfUser(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer_detailed
        return CommentSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        conditions = {
            "author__username": self.kwargs["username"],
            "id": self.kwargs["c_id"],
        }
        return get_object_or_404(queryset, **conditions)

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
