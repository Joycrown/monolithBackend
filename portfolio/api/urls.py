from django.urls import path, include
from django.conf.urls import url
from .views import (
    CreditCardCreateView,
    CreditCardDetailView,
    CreditCardUpdateView,
    FiatWalletDetailView,
    FiatWalletUpdateView,
    DepositView,
    WithdrawView,
    ConversionView,
    StockTransactionsDetailView,
    PortfolioHistory,
    CreateStockOrder,
    StockWalletDetailView,
    FiatWalletTransactionsDetailView,
    StockTransactionsDetailView,
    FiatWalletTransactionsDetailView,
    BankCreateView,
    BankRetrieveView,
    BankUpdateView,
    BankDestroyAPIView,
    CreditCardDestroyAPIView,
    FiatWalletDestroyView,
    CryptoTransactionsDetailView,
    CryptoWalletDetailView,
    CreateCryptoOrder,
    AccountStatementViewSet,
    WatchlistDetailView,
    WatchlistUpdateView,
    DeleteWatchlistView
)

app_name = "portfolio"


urlpatterns = [
    path("creditcard/", CreditCardCreateView.as_view(), name="create-credit-card"),
    path(
        "creditcard/<slug>/retrieve",
        CreditCardDetailView.as_view(),
        name="retrieve-credit-card",
    ),
    path(
        "creditcard/<slug>/update",
        CreditCardUpdateView.as_view(),
        name="update-credit-card",
    ),
    path(
        "creditcard/<slug>/delete",
        CreditCardDestroyAPIView.as_view(),
        name="delete-credit-card",
    ),
    path("bank/", BankCreateView.as_view(), name="create-bank"),
    path(
        "bank/<slug>/retrieve",
        BankRetrieveView.as_view(),
        name="retrieve-bank",
    ),
    path(
        "bank/<slug>/update",
        BankUpdateView.as_view(),
        name="update-bank",
    ),
    path(
        "bank/<slug>/delete",
        BankDestroyAPIView.as_view(),
        name="delete-bank",
    ),
    path(
        "wallet/<slug>/retrieve", FiatWalletDetailView.as_view(), name="retrieve-wallet"
    ),
    path("wallet/<slug>/update",
         FiatWalletUpdateView.as_view(), name="update-wallet"),
    path("wallet/<slug>/delete",
         FiatWalletDestroyView.as_view(), name="delete-wallet"),
    path(
        "stock-wallet/<slug>/retrieve",
        StockWalletDetailView.as_view(),
        name="retrieve-stock-wallet",
    ),
    path("deposit", DepositView.as_view(), name="deposit"),
    path("withdrawal", WithdrawView.as_view(), name="withdraw"),
    path("conversion", ConversionView.as_view(), name="convert"),
    path(
        "fiat-transaction/<slug>/retrieve",
        FiatWalletTransactionsDetailView.as_view(),
        name="fiat-transaction",
    ),
    path(
        "stock-transaction/<slug>/retrieve",
        StockTransactionsDetailView.as_view(),
        name="stock-transaction",
    ),
    path(
        "portfolio-history/",
        PortfolioHistory.as_view(),
        name="portfolio-history",
    ),
    path(
        "stock-order/create",
        CreateStockOrder.as_view(),
        name="portfolio-history",
    ),
    path(
        "crypto-wallet/<slug>/retrieve",
        CryptoWalletDetailView.as_view(),
        name="retrieve-crypto-wallet",
    ),
    path(
        "crypto-transaction/<slug>/retrieve",
        CryptoTransactionsDetailView.as_view(),
        name="crypto-transaction",
    ),
    path(
        "crypto-order/create",
        CreateCryptoOrder.as_view(),
        name="crypto-order",
    ),
    path('account_statements/', AccountStatementViewSet.as_view(
        {'get': 'list'}), name='account_statements_list'),
    path('account_statements/<slug:slug>/', AccountStatementViewSet.as_view(
        {'get': 'retrieve'}), name='account_statements_detail'),

    path('watchlist/', WatchlistDetailView.as_view(), name='watchlist_detail'),
    path('watchlist/update/', WatchlistUpdateView.as_view(),
         name='watchlist_update'),
    path('watchlist/delete/', DeleteWatchlistView.as_view(),
         name='watchlist_delete'),
]
