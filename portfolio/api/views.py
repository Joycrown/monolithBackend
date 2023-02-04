import requests
import random
import string
from django.urls import reverse

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView,
)
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from portfolio.utils import Rave, SECRET_KEY, ENCRYPTION_KEY, convert
from portfolio.models import (
    FiatWallet,
    Cash,
    CreditCard,
    Transactions,
    Bank,
    StockWallet,
    StockTransaction,
    CryptoWallet,
    CryptoTransaction,
    AccountStatement,
)
from .serializers import (
    CreditCardSerializer,
    FiatWalletSerializer,
    BankSerializer,
    OrderSerializer,
    StockWalletSerializer,
    FiatTransactionSerializer,
    StockTransactionSerializer,
    CryptoWalletSerializer,
    CryptoTransactionSerializer,
    AccountStatementSerializer,
)
from core.utils import get_broker_client
from alpaca.trading.client import TradingClient

# Credit Cars View


class CreditCardCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreditCardSerializer
    queryset = CreditCard.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreditCardDetailView(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = CreditCardSerializer
    queryset = CreditCard.objects.all()


class StockWalletDetailView(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = StockWalletSerializer
    queryset = StockWallet.objects.all()


class CreditCardUpdateView(UpdateAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = CreditCardSerializer
    queryset = CreditCard.objects.all()


class CreditCardDestroyAPIView(DestroyAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = CreditCardSerializer
    queryset = CreditCard.objects.all()


# Fiat Wallet View
class FiatWalletDetailView(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = FiatWalletSerializer
    queryset = FiatWallet.objects.all()


class StockTransactionsDetailView(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = StockTransactionSerializer
    queryset = StockTransaction.objects.all()


class FiatWalletTransactionsDetailView(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = FiatTransactionSerializer
    queryset = Transactions.objects.all()


class FiatWalletUpdateView(UpdateAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = FiatWalletSerializer
    queryset = FiatWallet.objects.all()


class FiatWalletDestroyView(DestroyAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = FiatWalletSerializer
    queryset = FiatWallet.objects.all()


class BankCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BankSerializer
    queryset = Bank.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankRetrieveView(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = BankSerializer
    queryset = Bank.objects.all()


class BankUpdateView(UpdateAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = BankSerializer
    queryset = Bank.objects.all()


class BankDestroyAPIView(DestroyAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = BankSerializer
    queryset = Bank.objects.all()


class DepositView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def bank(self, request, q):
        try:
            bnk = Bank.objects.filter(user=request.user).first()
            data = request.data
            payload = {
                "account_number": bnk.account_number,
                "currency": data["currency"],
                "amount": data["amount"],
                "fullname": bnk.fullname,
                "email": bnk.email,
                "account_bank": bnk.account_bank,
            }

            # BVN required for UBA aacounts
            if data["account_bank"] == "033":
                payload["bvn"] = data["bvn"]

            rave = Rave(secret_key=SECRET_KEY, encryption_key=ENCRYPTION_KEY)
            charge_response = rave.charge_bank_ng(payload)

            if charge_response and charge_response["status"] == "success":
                return Response(
                    data={
                        "status": "successful",
                        "message": "Payment initiated successfully",
                        "data": charge_response,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                data={
                    "status": "error",
                    "message": "There was a problem",
                    "data": charge_response,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except KeyError as e:
            return Response(
                data={
                    "status": "error",
                    "message": f"Payload is missing the following field: {e}",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def credit_card(self, request, q):
        if q["payment"] == "charge":
            try:
                data = request.data
                crd = CreditCard.objects.filter(user=request.user).first()

                payload = {
                    "card_number": crd.card_number,
                    "cvv": crd.cvv,
                    "expiry_month": crd.expiry_month,
                    "expiry_year": crd.expiry_year,
                    "currency": data["currency"],
                    "amount": data["amount"],
                    # "tx_ref": data["tx_ref"],
                    "fullname": crd.fullname,
                    "email": crd.email,
                    "redirect_url": data["redirect_url"],
                }

                if "authorization" in data:
                    payload["authorization"] = data["authorization"]

                rave = Rave(secret_key=SECRET_KEY,
                            encryption_key=ENCRYPTION_KEY)
                charge = rave.charge_card(payload)

                if charge and charge["status"] == "success":
                    txn = Transactions.objects.create(
                        customer=requests.user, credit_card=crd
                    )
                    txn.transaction_id = charge["data"]["id"]
                    # txn.transaction_id = charge["data"]["id"]
                    txn.amount_paid = charge["data"]["amount"]
                    txn.currency = charge["data"]["currency"]
                    txn.status = charge["data"]["status"]
                    return Response(
                        data={
                            "status": "successful",
                            "message": "Payment initiated successfully",
                            "data": charge,
                        },
                        status=status.HTTP_200_OK,
                    )

                return Response(
                    data={
                        "status": "error",
                        "message": "There was a problem",
                        "data": charge,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            except KeyError as e:
                return Response(
                    data={
                        "status": "error",
                        "message": f"Payload is missing the following field: {e}",
                        "data": None,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif q["payment"] == "validate":
            try:
                data = request.data
                flw_ref = data["flw_ref"]
                otp = data["otp"]

                rave = Rave(secret_key=SECRET_KEY,
                            encryption_key=ENCRYPTION_KEY)
                validation = rave.validate_charge(flw_ref, otp)

                if validation and validation["status"] == "success":
                    return Response(
                        data={
                            "status": "successful",
                            "message": "Payment validated successfully",
                            "data": validation,
                        },
                        status=status.HTTP_200_OK,
                    )

                return Response(
                    data={
                        "status": "error",
                        "message": "There was a problem",
                        "data": validation,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            except KeyError as e:
                return Response(
                    data={
                        "status": "error",
                        "message": f"Payload is missing the following field: {e}",
                        "data": None,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif q["payment"] == "verify":

            try:
                # query_params = request.GET
                rave = Rave(SECRET_KEY, ENCRYPTION_KEY)
                verification_response = rave.verify_transaction(str(q["id"]))

                assert verification_response["data"]["status"] == "successful"
                assert verification_response["data"]["currency"] == q["currency"]
                assert verification_response["data"]["tx_ref"] == q["txref"]
                assert int(verification_response["data"]["charged_amount"]) >= int(
                    q["amount"]
                )
                customer = Transactions.get_customer_id_via_charge_id(q["id"])
                customer.status = verification_response["data"]["status"]
                customer.save()
                fiat = FiatWallet.objects.filter(user=customer)
                cash = fiat.cash.filter(currency_type="NGN").first()
                cash.amount += verification_response["data"]["charged_amount"]
                cash.save()

                return Response(
                    data={
                        "status": "successful",
                        "message": "Payment verified",
                        "data": verification_response,
                    },
                    status=status.HTTP_200_OK,
                )

            except AssertionError:
                return Response(
                    data={
                        "status": "error",
                        "message": "Payment not verified",
                        "data": verification_response,
                    },
                    status=status.HTTP_409_CONFLICT,
                )

            except KeyError:
                return Response(
                    data={
                        "status": "error",
                        "message": "Check your query parameters. Bad request.",
                        "data": None,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def post(self, request):

        q = request.GET
        if q["deposit"] == "bank":
            self.bank(request, q)
        elif q["deposit"] == "creditcard":
            self.credit_card(request, q)


class WithdrawView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        pass


class ConversionView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        # colect to currency and value from the client

        to_val = convert(data["currency"], data["amount"])
        return Response(
            data={
                "status": "successful",
                "message": "Payment verified",
                "data": {"currrency": data["currency"], "value": to_val},
            },
            status=status.HTTP_200_OK,
        )


class CreateStockOrder(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        acc_id = request.user.investor.account_id
        broker_client = get_broker_client()

        order = broker_client.submit_order_for_account(acc_id, data)
        return Response({"status": True, "data": order}, status.HTTP_200_OK)


class PortfolioHistory(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = request.data
        acc_id = request.user.investor.account_id
        broker_client = get_broker_client()

        history = broker_client.get_portfolio_history_for_account(acc_id)
        return Response({"status": True, "data": history}, status.HTTP_200_OK)


class CreateCryptoOrder(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        acc_id = request.user.investor.account_id
        broker_client = get_broker_client()

        order = broker_client.submit_order_for_account(acc_id, data)
        return Response({"status": True, "data": order}, status.HTTP_200_OK)


class CryptoWalletDetailView(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = CryptoWalletSerializer,
    queryset = CryptoWallet.objects.all()


class CryptoTransactionsDetailView(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    serializer_class = CryptoTransactionSerializer
    queryset = CryptoTransaction.objects.all()


class AccountStatementViewSet(RetrieveAPIView):
    lookup_url_kwarg = "slug"
    permission_classes = (IsAuthenticated,)
    queryset = AccountStatement.objects.all()
    serializer_class = AccountStatementSerializer
