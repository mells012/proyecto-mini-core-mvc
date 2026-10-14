from rest_framework.routers import DefaultRouter

from .views import (
    ComisionCalculadaViewSet,
    ReglaComisionViewSet,
    VendedorViewSet,
    VentaViewSet,
)

router = DefaultRouter()
router.register(r"vendedores", VendedorViewSet, basename="vendedor")
router.register(r"reglas", ReglaComisionViewSet, basename="regla")
router.register(r"ventas", VentaViewSet, basename="venta")
router.register(
    r"comisiones-calculadas", ComisionCalculadaViewSet, basename="comision-calculada"
)

urlpatterns = router.urls
