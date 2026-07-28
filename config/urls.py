from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from catalog.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("auth/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("tienda/", include("catalog.urls")),
    path("pedidos/", include("orders.urls")),
    path("dashboard/", include("dashboard.urls")),
]

# Sirve archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
