from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="LFG API",
        default_version='1.0.0',
        description="LFG API Endpoints",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes = []
)

urlpatterns = [
    path('', RedirectView.as_view(url='admin/')),
    path("admin/", admin.site.urls),
    path('api/v1/', include('lfg_api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema")
]
