from rest_framework.fields import CurrentUserDefault
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
 
from core.models import User, Feedback, Investor, Poi, Document
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import render, get_object_or_404

from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        "username": "The username should only contain alphanumeric characters"
    }

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class VerifyOTPRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "otp", "tokens", "username", "slug" ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        otp = attrs.get("otp", "")

        user = User.objects.filter(email=email).first()
        refresh = RefreshToken.for_user(user=user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")   
        if user.otp != otp:
            raise AuthenticationFailed("The OTP Code is invalid")                             

        return {"id": user.id, "email": user.email, "username":user.username, "slug": user.slug, "tokens": user.tokens, "refresh_token": refresh_token, "access_token": access_token}


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "tokens"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")
                                

        return {"email": user.email}

        return super().validate(attrs)


class VerifyOTPLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "otp", "tokens", "username", "slug" ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        otp = attrs.get("otp", "")

        user = User.objects.filter(email=email).first()
        refresh = RefreshToken.for_user(user=user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")                            
        if user.otp != otp:
            raise AuthenticationFailed("The OTP Code is invalid")                             
        
        return {"id": user.id, "email": user.email, "username":user.username, "slug": user.slug, "tokens": user.tokens, "refresh_token": refresh_token, "access_token": access_token}



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class VerifyOTPResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "otp", "username", "slug" ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        otp = attrs.get("otp", "")

        user = User.objects.filter(email=email).first()

        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")                            
        if user.otp != otp:
            raise AuthenticationFailed("The OTP Code is invalid")                             

        return {"id": user.id, "email": user.email, "username":user.username, "slug": user.slug}



class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        
        user = User.objects.filter(email=email).first()

        if not user.is_active:
            raise AuthenticationFailed("Account has been disabled")
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ["email", "password"]

    def validate(self, attrs):
        try:
            email = attrs.get("email")
            password = attrs.get("password")

            user = User.objects.filter(email=email).first()
            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The otp is invalid", 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "name",
            "call_code",
            "phone",
            "bio",
            "sex",
            "avatar",
            "cover",
            "website",
            "country",
            "state",
            "address",
            "city",
            "location",
            "day",
            "month",
            "year",
            "dob",
            "address",
            "city",
            "state",
            "otp",
            "push_token",
            "followers_count",
            "followers",
            "following_count",
            "following",
            "is_block_member",
            "is_block_moderator",
            "is_verified",
            "is_active",
            "active",
            "is_staff",
            "is_admin",
            "is_banned",
            "is_investor",
            "tos",
            "slug",
            "created",
            "created_at",
        )


class UserCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "followers_count",
            "following_count"
            )

class UserLessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "avatar", "bio"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("id", "title", "text", "user", "created_on")


class PoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poi
        fields = ("id", "user", "id_type", "content", "created_on")


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "user", "file", "doc_type", "created_on")


class InvestorSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField()
    account_id = serializers.ReadOnlyField()

    class Meta:
        model = Investor
        fields = (
            "id",
            "user",
            "account_id",
            "name",
            "watchlist_id",
            "professional_status",
            "professional_cat",
            "professional_subcat",
            "income",
            "slug",
            "experience",
            "created_at",
        )


class UserProfileSerializer(serializers.ModelSerializer):

    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_self = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "name",
            "call_code",
            "phone",
            "bio",
            "sex",
            "avatar",
            "cover",
            "website",
            "country",
            "state",
            "address",
            "city",
            "location",
            "day",
            "month",
            "year",
            "dob",
            "otp",
            "followers_count",
            "followers",
            "following_count",
            "following",
            "is_block_member",
            "is_block_moderator",
            "is_verified",
            "is_active",
            "active",
            "is_staff",
            "is_admin",
            "is_banned",
            "is_investor",
            "slug",
            "tos",
            "is_self",
            "created",
            "created_at",
        )

    def get_is_self(self, user):
        if "request" in self.context:
            request = self.context["request"]
            if user.id == request.user.id:
                return True
            else:
                return False
        return False

    def get_following(self, obj):
        if "request" in self.context:
            request = self.context["request"]
            if obj in request.user.following.all():
                return True
        return False


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "name",
            "call_code",
            "phone",
            "bio",
            "sex",
            "avatar",
            "cover",
            "website",
            "country",
            "state",
            "address",
            "city",
            "location",
            "day",
            "month",
            "year",
            "dob",
            "otp",
            "followers_count",
            "followers",
            "following_count",
            "following",
            "is_block_member",
            "is_block_moderator",
            "is_verified",
            "is_active",
            "active",
            "is_staff",
            "is_admin",
            "is_banned",
            "is_investor",
            "slug",
            "tos",
            "tokens",
            "created",
            "created_at",
        )
        depth=1
