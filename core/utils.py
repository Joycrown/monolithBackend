from alpaca.broker.models import Contact, Identity, Disclosures, Agreement
from alpaca.trading.requests import CreateWatchlistRequest
from alpaca.broker.requests import (
    CreateAccountRequest,
    CreatePlaidRelationshipRequest,
    CreateACHTransferRequest,
    CreateJournalRequest,
    CreateBatchJournalRequest,
    MarketOrderRequest,
    LimitOrderRequest,
)
from alpaca.broker.enums import (
    TaxIdType,
    FundingSource,
    AgreementType,
    TransferDirection,
    TransferTiming,
)
from decouple import config


def get_broker_client():
    BROKER_API_KEY = config("APCA_BROKER_API_KEY")
    BROKER_SECRET_KEY = config("APCA_BROKER_API_SECRET")

    broker_client = BrokerClient(
        api_key=BROKER_API_KEY,
        secret_key=BROKER_SECRET_KEY,
        sandbox=True,
    )
    return broker_client


def create_broker_account(data, user, request):
    broker_client = get_broker_client()
    contact_data = Contact(
        email_address=user.email,
        phone_number=user.phone,
        street_address=[user.address],
        city=user.city,
        state=user.state,
        postal_code=user.postal_code,
        country=user.country,
    )
    # Identity
    identity_data = Identity(
        given_name=data["given_name"],
        middle_name=data["middle_name"](),
        family_name=user.get_last_name(),
        date_of_birth=str(user.dob),
        country_of_citizenship=user.country,
        country_of_birth=user.country,
        country_of_tax_residence=user.country,
        funding_source=[FundingSource.EMPLOYMENT_INCOME],
    )

    # Disclosures
    disclosure_data = Disclosures(
        is_control_person=False,
        is_affiliated_exchange_or_finra=False,
        is_politically_exposed=False,
        immediate_family_exposed=False,
    )

    # Agreements
    agreement_data = [
        Agreement(
            agreement=AgreementType.MARGIN,
            signed_at=timezone.now(),
            ip_address=request.META.get("REMOTE_ADDR", ""),
        ),
        Agreement(
            agreement=AgreementType.ACCOUNT,
            signed_at=timezone.now(),
            ip_address=request.META.get("REMOTE_ADDR", ""),
        ),
        Agreement(
            agreement=AgreementType.CUSTOMER,
            signed_at=timezone.now(),
            ip_address=request.META.get("REMOTE_ADDR", ""),
        ),
        Agreement(
            agreement=AgreementType.CRYPTO,
            signed_at=timezone.now(),
            ip_address=request.META.get("REMOTE_ADDR", ""),
        ),
    ]

    # ## CreateAccountRequest ## #
    account_data = CreateAccountRequest(
        contact=contact_data,
        identity=identity_data,
        disclosures=disclosure_data,
        agreements=agreement_data,
    )

    # Make a request to create a new brokerage account
    account = broker_client.create_account(account_data)
    return account


def create_user_watchlist(request, account_id):
    broker_client = get_broker_client()
    account_id = str(account_id)
    name = "My Watchlist"
    symbols = ["AAPL", "BTC"]

    watchlist_data = CreateWatchlistRequest(
        name=name,
        symbols=symbols,
    )

    watchlist = broker_client.create_watchlist_for_account(
        account_id, watchlist_data)
    return watchlist
