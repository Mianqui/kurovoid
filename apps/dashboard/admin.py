from django.contrib import admin
from .models import ConfiguracionTienda

@admin.register(ConfiguracionTienda)
class ConfiguracionTiendaAdmin(admin.ModelAdmin):
    list_display = ("__str__", "precio_envio")
