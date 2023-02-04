from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import User, Investor
from django.utils import timezone
from alpaca.trading.client import TradingClient


CURRENCY_OPTIONS = (
    ("USD", "USD"),
    ("NGN", "NGN"),
)
ACCOUNT_TYPE = (("deposit", "deposit"), ("withdrawal", "withdrawal"))

# Create your models here.


class Cash(models.Model):

    currency_type = models.CharField(
        max_length=3, choices=CURRENCY_OPTIONS, default="NGN"
    )
    amount = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FiatWallet(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash = models.ManyToManyField(Cash)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def slug(self):
        return self.user.slug


class CreditCard(models.Model):
    user = models.ForeignKey(
        User, default=None, related_name="card", on_delete=models.CASCADE
    )
    cvv = models.CharField(null=False, max_length=3)
    card_number = models.CharField(null=False, max_length=20)
    brand = models.CharField(null=True, blank=True, max_length=20)
    exp_month = models.IntegerField(
        null=False, validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    exp_year = models.IntegerField(
        null=False, validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    name_on_card = models.CharField(null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def display_number(self):
        print(str(self.card_number)[-4:])
        return "XXXX XXXX XXXX " + str(self.card_number)[-4:]

    def slug(self):
        return self.user.slug


class Bank(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    account_number = models.CharField(
        max_length=32, blank=False, null=False, default=None
    )
    account_bank = models.CharField(
        max_length=32, blank=False, null=False, default=None
    )
    account_type = models.CharField(
        max_length=15,
        choices=ACCOUNT_TYPE,
        default="deposit",
    )

    def slug(self):
        return self.user.slug


class Stock(models.Model):
    asset = models.CharField(max_length=25, null=False, blank=False)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StockWallet(models.Model):
    investor = models.ForeignKey(
        Investor, default=None, blank=False, on_delete=models.CASCADE, null=False
    )
    asset = models.ManyToManyField(Stock)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def slug(self):
        return self.investor.user.slug


class StockTransaction(models.Model):
    investor = models.ForeignKey(
        Investor, default=None, blank=False, on_delete=models.CASCADE, null=False
    )
    type = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(
        max_length=32, editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def slug(self):
        return self.investor.user.slug


class Transactions(models.Model):

    customer = models.ForeignKey(
        User, default=None, blank=False, on_delete=models.CASCADE, null=False
    )
    transaction_id = models.CharField(
        max_length=32, editable=False, null=False
    )  # Flutterwave charge id
    credit_card = models.ForeignKey(
        CreditCard, default=None, blank=True, on_delete=models.CASCADE, null=True
    )
    currency = models.CharField(
        max_length=3, default="NGN", editable=False, null=False)
    amount_paid = models.DecimalField(
        validators=[MinValueValidator(0)],
        null=False,
        default=0,
        decimal_places=2,
        max_digits=30,
    )
    transaction_fee = models.DecimalField(
        validators=[MinValueValidator(0)],
        null=False,
        default=0,
        decimal_places=2,
        max_digits=20,
    )
    exchange_rate = models.DecimalField(
        validators=[MinValueValidator(0)],
        null=False,
        default=0,
        decimal_places=2,
        max_digits=10,
    )
    receipt_url = models.CharField(
        max_length=250, editable=False, null=True, blank=True
    )
    status = models.CharField(
        max_length=32, editable=False, null=True, blank=True)

    def card_number_last_4(self):
        return self.credit_card.display_number()

    def card_brand(self):
        return self.credit_card.brand

    def card_expiry_month(self):
        return self.credit_card.exp_month

    def card_expiry_month(self):
        return self.credit_card.exp_month

    def card_expiry_year(self):
        return self.credit_card.exp_year

    def get_customer_id_via_charge_id(self, charge_id):
        return self.objects.filter(transaction_id=charge_id).customer

    def slug(self):
        return self.customer.slug


class Crypto(models.Model):
    asset = models.CharField(max_length=25, null=False, blank=False)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CryptoWallet(models.Model):
    investor = models.ForeignKey(
        Investor, default=None, blank=False, on_delete=models.CASCADE, null=False
    )
    asset = models.ManyToManyField(Crypto)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def slug(self):
        return self.investor.user.slug


class CryptoTransaction(models.Model):
    investor = models.ForeignKey(
        Investor, default=None, blank=False, on_delete=models.CASCADE, null=False
    )
    type = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(
        max_length=32, editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def slug(self):
        return self.investor.user.slug


class AccountStatement(models.Model):

    DOC_TYPE_CHOICES = (
        ('account_statement', 'Account Statement'),
        ('trade_confirmation', 'Trade Confirmation'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    statement_start_date = models.DateField()
    statement_end_date = models.DateField()
    statement_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)

    def slug(self):
        return self.user.slug
