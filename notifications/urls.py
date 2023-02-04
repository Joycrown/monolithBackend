from django.urls import path, include
from django.conf.urls import url
from .views import NotificationView, NotificationSeen

app_name = "notifications"

urlpatterns = [
    path('notification_list/', NotificationView, name='notification-list'),
    path('notification_seen_delete/',
         NotificationSeen.as_view(), name='notification-seen'),
]