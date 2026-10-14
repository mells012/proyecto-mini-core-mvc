"""
Serializers: convierten los objetos del Modelo en JSON (y viceversa) para
que la API REST pueda entregarlos al frontend. Son parte de la capa de
"Vista" en DRF (arman la representacion de datos que la vista devuelve).
"""

from rest_framework import serializers

from .models import ComisionCalculada, ReglaComision, Vendedor, Venta


class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ["id", "nombre", "email", "activo", "creado_en"]


class ReglaComisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReglaComision
        fields = ["id", "nombre", "monto_minimo", "porcentaje", "activo"]


class VentaSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.CharField(
        source="vendedor.nombre", read_only=True
    )
    comision_estimada = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = [
            "id",
            "vendedor",
            "vendedor_nombre",
            "monto",
            "fecha",
            "descripcion",
            "creado_en",
            "comision_estimada",
        ]

    def get_comision_estimada(self, obj):
        """Incluye automaticamente la comision calculada segun las reglas
        vigentes, sin necesidad de un endpoint aparte para previsualizarla."""
        regla = obj.calcular_regla_aplicada()
        if not regla:
            return None
        monto = float(obj.monto) * float(regla.porcentaje) / 100
        return round(monto, 2)

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El monto de la venta debe ser mayor a cero."
            )
        return value


class ComisionCalculadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComisionCalculada
        fields = [
            "id",
            "venta",
            "regla_aplicada",
            "monto_comision",
            "calculado_en",
        ]


class RangoFechasSerializer(serializers.Serializer):
    """Valida el rango de fechas recibido para el calculo de comisiones."""

    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()

    def validate(self, data):
        if data["fecha_inicio"] > data["fecha_fin"]:
            raise serializers.ValidationError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )
        return data
