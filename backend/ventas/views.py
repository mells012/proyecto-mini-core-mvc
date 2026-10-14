"""
Views: en el patron MVT de Django esta es la capa que hace el trabajo del
"Controlador" de MVC. Recibe la peticion HTTP, aplica la logica de negocio
(usando los Modelos) y decide que datos devolver (via los Serializers).
"""

from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ComisionCalculada, ReglaComision, Vendedor, Venta
from .serializers import (
    ComisionCalculadaSerializer,
    RangoFechasSerializer,
    ReglaComisionSerializer,
    VendedorSerializer,
    VentaSerializer,
)


class VendedorViewSet(viewsets.ModelViewSet):
    """CRUD de vendedores. Permite ademas filtrar por ?activo=true."""

    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        activo = self.request.query_params.get("activo")
        if activo is not None:
            queryset = queryset.filter(activo=(activo.lower() == "true"))
        return queryset


class ReglaComisionViewSet(viewsets.ModelViewSet):
    """CRUD de reglas de comision."""

    queryset = ReglaComision.objects.all()
    serializer_class = ReglaComisionSerializer


class VentaViewSet(viewsets.ModelViewSet):
    """
    CRUD de ventas (crear, leer, eliminar - el CRUD que pide el ejercicio)
    mas el endpoint personalizado `calcular_comisiones` que es el nucleo
    funcional del Mini Core.
    """

    queryset = Venta.objects.select_related("vendedor").all()
    serializer_class = VentaSerializer

    def get_queryset(self):
        """Permite filtrar ventas por vendedor y/o rango de fechas via
        querystring: ?vendedor=<id>&fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD"""
        queryset = super().get_queryset()
        vendedor_id = self.request.query_params.get("vendedor")
        fecha_inicio = self.request.query_params.get("fecha_inicio")
        fecha_fin = self.request.query_params.get("fecha_fin")

        if vendedor_id:
            queryset = queryset.filter(vendedor_id=vendedor_id)
        if fecha_inicio:
            queryset = queryset.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha__lte=fecha_fin)
        return queryset

    @action(detail=False, methods=["post"], url_path="calcular-comisiones")
    def calcular_comisiones(self, request):
        """
        Endpoint clave del Mini Core.

        POST /api/ventas/calcular-comisiones/
        body: {"fecha_inicio": "YYYY-MM-DD", "fecha_fin": "YYYY-MM-DD"}

        Pasos:
            1. Validar el rango de fechas recibido.
            2. Obtener las ventas del periodo.
            3. Calcular la comision de cada venta en base a las reglas
               vigentes (la regla con el monto_minimo mas alto que la
               venta SI alcanza).
            4. Guardar cada calculo en ComisionCalculada (trazabilidad).
            5. Armar un reporte estructurado: resumen por vendedor +
               totales globales del periodo.
        """
        rango_serializer = RangoFechasSerializer(data=request.data)
        rango_serializer.is_valid(raise_exception=True)
        fecha_inicio = rango_serializer.validated_data["fecha_inicio"]
        fecha_fin = rango_serializer.validated_data["fecha_fin"]

        ventas_periodo = (
            Venta.objects.select_related("vendedor")
            .filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)
            .order_by("vendedor__nombre", "fecha")
        )

        resumen_por_vendedor = {}
        total_ventas_global = 0
        total_comision_global = 0

        for venta in ventas_periodo:
            regla = venta.calcular_regla_aplicada()
            monto_venta = float(venta.monto)

            if regla:
                monto_comision = round(
                    monto_venta * float(regla.porcentaje) / 100, 2
                )
                ComisionCalculada.objects.create(
                    venta=venta,
                    regla_aplicada=regla,
                    monto_comision=monto_comision,
                )
            else:
                monto_comision = 0

            vendedor_id = venta.vendedor_id
            if vendedor_id not in resumen_por_vendedor:
                resumen_por_vendedor[vendedor_id] = {
                    "vendedor_id": vendedor_id,
                    "vendedor_nombre": venta.vendedor.nombre,
                    "total_ventas": 0,
                    "cantidad_ventas": 0,
                    "total_comision": 0,
                    "detalle_ventas": [],
                }

            resumen_por_vendedor[vendedor_id]["total_ventas"] += monto_venta
            resumen_por_vendedor[vendedor_id]["cantidad_ventas"] += 1
            resumen_por_vendedor[vendedor_id]["total_comision"] += monto_comision
            resumen_por_vendedor[vendedor_id]["detalle_ventas"].append(
                {
                    "venta_id": venta.id,
                    "fecha": venta.fecha,
                    "monto": monto_venta,
                    "regla_aplicada": regla.nombre if regla else None,
                    "porcentaje": float(regla.porcentaje) if regla else 0,
                    "comision": monto_comision,
                }
            )

            total_ventas_global += monto_venta
            total_comision_global += monto_comision

        # Redondeos finales para presentacion.
        for resumen in resumen_por_vendedor.values():
            resumen["total_ventas"] = round(resumen["total_ventas"], 2)
            resumen["total_comision"] = round(resumen["total_comision"], 2)

        reporte = {
            "periodo": {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
            },
            "cantidad_vendedores": len(resumen_por_vendedor),
            "cantidad_ventas": ventas_periodo.count(),
            "total_ventas_global": round(total_ventas_global, 2),
            "total_comision_global": round(total_comision_global, 2),
            "resumen_por_vendedor": list(resumen_por_vendedor.values()),
        }

        return Response(reporte, status=status.HTTP_200_OK)


class ComisionCalculadaViewSet(viewsets.ReadOnlyModelViewSet):
    """Historial de comisiones calculadas (solo lectura, para trazabilidad)."""

    queryset = ComisionCalculada.objects.select_related(
        "venta", "regla_aplicada"
    ).all()
    serializer_class = ComisionCalculadaSerializer
