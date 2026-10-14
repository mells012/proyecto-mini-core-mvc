"""
URLs raiz del proyecto.

/admin/   -> panel de administracion de Django
/api/     -> API REST consumida por el frontend en React
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse({"status": "ok", "proyecto": "Mini Core - Ventas y Comisiones"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("ventas.urls")),
    path("", health_check),
]
