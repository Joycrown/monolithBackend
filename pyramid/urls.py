from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.api.urls")),
    path("block/", include("block.api.urls")),
    path("core/", include("core.api.urls")),
    #path("chat/", include("chat.urls")),
    path("search/", include("search.api.urls")),
    path("notifications/", include("notifications.urls")),
    #path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    #path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
