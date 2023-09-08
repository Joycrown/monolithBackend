from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions


urlpatterns = [
    path("babla/", admin.site.urls),
    path("block/", include("block.api.urls")),
    path("core/", include("core.api.urls")),
    path("chat/", include("message.urls")),
    path("search/", include("search.api.urls")),
    path("chamber/", include("chamber.urls")),
    path("events/", include("events.urls")),
    path("newsletters/", include("newsletters.urls")),
    path("notifications/", include("notifications.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
