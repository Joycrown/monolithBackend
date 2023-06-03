from django.urls import path, include
from django.conf.urls import url
from .views import (
    UserIDView,
    RegisterView,
    ResendRegisterEmailView,
    VerifyEmail, 
    LoginAPIView,
    ResendLoginEmailView,
    VerifyLoginEmail,
    ResetPasswordAPIView,
    ResendResetPasswordView,
    VerifyResetEmail,
    SetNewPasswordAPIView,
    LogoutAPIView,
    follow_unfollow_user,
    UserFollowers,
    UserFollowing,
    user_followed_user,
    ChangePassword,
    PoiCreateView,
    DocumentCreateView,
    FeedbackCreateView,
    InvestorDeleteView,
    InvestorUpdateView,
    InvestorCreateView,
    InvestorDetailView,
    UserUpdateView,
    UserDetailView,
    UserDeleteView,
    UpdateUserView,
    BrokerAccountDetailView,
    BrokerAccountUpdateView,
    BrokerAccountDeleteView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path("user-id/", UserIDView.as_view(), name="user-id"),
    path("register/", RegisterView.as_view(), name="register"),
    path("resend-register-code/", ResendRegisterEmailView.as_view(), name="resend-register-code"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("resend-login-code/", ResendLoginEmailView.as_view(), name="resend-login-code"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("resend-reset-code/", ResendResetPasswordView.as_view(), name="resend-reset-code"),
    path("set-new-password/", SetNewPasswordAPIView.as_view(), name="set-new-password"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("email-login-verify/", VerifyLoginEmail.as_view(), name="email-login-verify"),
    path("email-reset-verify/", VerifyResetEmail.as_view(), name="email-reset-verify"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),    
    path("poi/create/", PoiCreateView.as_view(), name="poi-create"),
    path("document/create/", DocumentCreateView.as_view(), name="document-create"),
    path("feedback/create/", FeedbackCreateView.as_view(), name="feedback-create"),
    path("investor/create/", InvestorCreateView.as_view(), name="investor-create"),
    path(
        "investor/update/", InvestorUpdateView.as_view(), name="investor-update"
    ),
    path(
        "investor/delete/", InvestorDeleteView.as_view(), name="investor-delete"
    ),
    path("investor/retrieve/", InvestorDetailView.as_view(), name="investor-detail"),
    path(
        "user/update/<username>/", UserUpdateView.as_view(), name="user-update"
    ),
    path(
        "user/delete/<username>/", UserDeleteView.as_view(), name="user-delete"
    ),
    path("user/detail/<username>/", UpdateUserView.as_view(), name="user-detail"),
    path("user/retrieve/<username>/", UserDetailView.as_view(), name="user-detail"),
    path("follow/user/", follow_unfollow_user, name="follow_unfollow_user"),
    path("followers/<username>/", UserFollowers.as_view(), name="user_followers"),
    path("following/<username>/", UserFollowing.as_view(), name="user_following"),
    path("user/followed/user/", user_followed_user, name="user_followed_user"),
    path("password/<username>/", ChangePassword.as_view(), name="change"),
    path(
        "broker_account/detail/",
        BrokerAccountDetailView.as_view(),
        name="broker_account-detail",
    ),
    path(
        "broker_account/update/",
        BrokerAccountUpdateView.as_view(),
        name="broker_account-update",
    ),
    path(
        "broker_account/delete/",
        BrokerAccountDeleteView.as_view(),
        name="broker_account-delete",
    ),
]
