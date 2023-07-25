import uuid

from utils.utils import get_random_code
from utils.utils import MONTH as month
from block.models import Block

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken

# TODO Add the users wallet when working on crypto/stock/payment system


def upload_to(instance, filename):
    return "avatars/{0}/{1}".format(instance.username, filename)


def upload_for(instance, filename):
    return "covers/{0}/{1}".format(instance.username, filename)


def document_to(instance, filename):
    return "documents/{0}/{1}".format(instance.user.username, filename)

def add_user_util(instance):
    
    now = date.today()
    if not instance.month:
        instance.day = now.day
        instance.month = month[now.month]
        instance.year = now.year
        instance.created = date(day=now.day, month=now.month, year=now.year)

class UserManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not phone:
            raise ValueError("Users must have a phone number")        

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, phone, password=None):
        user = self.create_user(email, username, phone, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    cover = models.ImageField(upload_to=upload_for, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=1000, blank=True)
    bio = models.TextField(blank=True, null=True)
    sex = models.CharField(max_length=32, null=True, blank=True)
    call_code = models.CharField(max_length=500, null=True, blank=True)
    otp = models.IntegerField(blank=True, null=True, default=0)
    website = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=1000, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)
    day = models.CharField(max_length=3, null=True, blank=True)
    month = models.CharField(max_length=15, null=True, blank=True)
    year = models.CharField(max_length=7, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    dob = models.CharField(max_length=1000, null=True, blank=True)
    push_token = models.TextField(default="", blank=True, null=True)
    followers = models.ManyToManyField("self", related_name="user_followers", blank=True, symmetrical=False)
    following = models.ManyToManyField("self", related_name="user_following", blank=True, symmetrical=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, null=False, max_length=1000)
    tos = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created = models.CharField(max_length=1000, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone"]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()

    @property
    def is_block_member(self):
        return Block.objects.filter(subscribers=self)

    @property
    def is_block_moderator(self):
        return Block.objects.filter(moderators=self)
    
    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        ex = False
        SIZE = 250, 250
        if self.username:
            to_slug = slugify(str(self.username))
            ex = User.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + "" + str(get_random_code()))
                ex = User.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.username)
        self.slug = to_slug
        add_user_util(self)
        super().save(*args, **kwargs)


class Investor(models.Model):

    watchlist_id = models.CharField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="investor", editable=False
    )
    name = models.CharField(max_length=1000, blank=True)
    account_id = models.CharField(max_length=1000, blank=True, null=True)
    middle_name = models.CharField(max_length=1000, blank=True, null=True)
    given_name = models.CharField(max_length=1000, blank=True, null=True)
    professional_status = models.CharField(max_length=1000, blank=True)
    professional_cat = models.CharField(max_length=1000, null=True, blank=True)
    professional_subcat = models.CharField(max_length=1000, null=True, blank=True)
    income = models.CharField(max_length=1000, null=True, blank=True)
    experience = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def slug(self):
        return self.user.slug

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} has investor profile {self.name}"


class Feedback(models.Model):
    title = models.CharField(max_length=10000, blank=True, null=True)
    text = models.TextField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} gave feedback {self.title}"


# Users proof of identity
class Poi(models.Model):
    id_type = models.CharField(max_length=30000)
    content = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}'s proof of identity {self.id_type}"


# Users Legal documents
class Document(models.Model):
    file = models.FileField(upload_to=document_to, blank=True, null=True)
    doc_type = models.CharField(max_length=30000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}'s legal documents {self.doc_type}"
