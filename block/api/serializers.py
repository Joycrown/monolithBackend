from rest_framework import serializers
from block.models import *

from core.models import User
from core.api.serializers import UserLessInfoSerializer
from drf_extra_fields.fields import Base64ImageField, Base64FileField


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="get_username")

    class Meta:
        model = User
        fields = ("username",)


class BlockDetailSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()
    cover = Base64ImageField()

    class Meta:
        model = Block
        fields = [
            "id",
            "avatar",
            "cover",
            "name",
            "desc",
            "about",
            "day",
            "month",
            "year",
            "category",
            "block_type",
            "subscribers",
            "moderators",
            "creator",
            "created",
            "subscriber_count",
            "is_deleted",
            "slug",
            "numPosts",
            "online_count",
        ]
        depth = 1


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = "__all__"


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ("text",)


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("id", "block", "title", "text")


class LinkSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Link
        fields = ("id", "block", "image", "title", "url")


def voted(user, comment, value):
    return user.is_active and bool(user.vote_set.filter(comment=comment, value=value))


def voted_post(user, post, value):
    return user.is_active and bool(user.vote_set.filter(post=post, value=value))


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer_detailed(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "parent_comment",
            "report",
            "saved",
            "created",
            "text",
            "is_deleted",
            "saved_count",
            "report_count",
            "share_count",
            "voters",
            "votes",
            "saved_count",
            "report_count",
            "child_comments",
            "created_time_ago",
        ]
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer_detailed(serializers.ModelSerializer):
    attachment = Base64ImageField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "block",
            "attachment",
            "created",
            "link",
            "text",
            "post_type",
            "parent",
            "author",
            "report",
            "saved",
            "share_count",
            "saved_count",
            "report_count",
            "is_deleted",
            "is_repost",
            "is_reviewed",
            "voters",
            "votes",
            "reposts",
            "comments",
            "slug",
            "created_time_ago",
        ]
        depth = 2


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class AnonPostSerializer(serializers.ModelSerializer):
    author = UserLessInfoSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "author"]


class LessCommentSerializer(serializers.ModelSerializer):
    post_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "post_id"]

    def get_post_id(self, obj):
        return obj.post.id
