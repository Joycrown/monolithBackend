from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User
from portfolio.models import FiatWallet, CryptoWallet


@receiver(post_save, sender=User)
def post_save_user_wallet(sender, **kwargs):
	user = sender
    fiat = FiatWallet.objects.create(user=user)
    fiat.save()


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        CryptoWallet.objects.create(user=instance)
