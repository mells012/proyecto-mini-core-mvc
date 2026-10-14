from django.contrib import admin

from .models import ComisionCalculada, ReglaComision, Vendedor, Venta


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "email", "activo")
    search_fields = ("nombre",)


@admin.register(ReglaComision)
class ReglaComisionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "monto_minimo", "porcentaje", "activo")


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "vendedor", "monto", "fecha")
    list_filter = ("vendedor", "fecha")


@admin.register(ComisionCalculada)
class ComisionCalculadaAdmin(admin.ModelAdmin):
    list_display = ("id", "venta", "regla_aplicada", "monto_comision", "calculado_en")
