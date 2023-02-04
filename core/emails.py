from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template

import random
from utils.utils import Util

from .models import User

#TODO Add email template

def send_otp(email):
    subject = "Account Verification Email From Pyramid"
    otp = random.randint(1000, 9999)
    message = f"Your OTP is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message, email_from,[email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()

def send_login_otp(email):
    subject = "Login Email From Pyramid"
    otp = random.randint(1000, 9999)
    message = f"Your OTP is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message, email_from,[email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()

def send_reset_otp(email):
    subject = "Account Password Reset Email From Pyramid"
    otp = random.randint(1000, 9999)
    message = f"Your OTP is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message, email_from,[email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()   

