"""
Modelos del Mini Core de Ventas y Comisiones.

En el patron MVT de Django, esta capa corresponde al "Modelo": define la
estructura de la base de datos (tablas, campos y relaciones), tal como el
"Modelo" lo hace en el patron MVC clasico.

Tablas relacionadas del ejercicio (tres, como pide la asignacion):
    1. Vendedor
    2. ReglaComision
    3. Venta

Se agrega una cuarta tabla, ComisionCalculada, para dejar trazabilidad de
cada calculo realizado (historial), de forma analoga al proyecto de
referencia explicado en el video de semestres pasados.
"""

from django.db import models


class Vendedor(models.Model):
    """Informacion basica de cada vendedor."""

    nombre = models.CharField(max_length=120, unique=True)
    email = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class ReglaComision(models.Model):
    """
    Reglas configurables de comision.

    Cada regla define un porcentaje de comision que se aplica cuando el
    monto de una venta es mayor o igual al monto minimo configurado.
    Para calcular la comision de una venta se busca la regla con el
    monto_minimo mas alto que la venta SI alcanza.
    """

    nombre = models.CharField(max_length=80)
    monto_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["-monto_minimo"]

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}% desde ${self.monto_minimo})"


class Venta(models.Model):
    """
    Registro de una transaccion de venta.

    Relacion uno a muchos: un Vendedor puede tener muchas Ventas.
    """

    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, related_name="ventas"
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Venta #{self.id} - {self.vendedor.nombre} - ${self.monto}"

    def calcular_regla_aplicada(self):
        """
        Devuelve la ReglaComision con mayor monto_minimo que esta venta
        SI alcanza a cubrir, o None si no cumple ninguna regla.
        """
        return (
            ReglaComision.objects.filter(
                activo=True, monto_minimo__lte=self.monto
            )
            .order_by("-monto_minimo")
            .first()
        )


class ComisionCalculada(models.Model):
    """
    Historial de comisiones calculadas: deja trazabilidad de cada
    calculo realizado sobre una venta en un momento dado.
    """

    venta = models.ForeignKey(
        Venta, on_delete=models.CASCADE, related_name="comisiones"
    )
    regla_aplicada = models.ForeignKey(
        ReglaComision, on_delete=models.SET_NULL, null=True, blank=True
    )
    monto_comision = models.DecimalField(max_digits=10, decimal_places=2)
    calculado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-calculado_en"]

    def __str__(self):
        return f"Comision ${self.monto_comision} - Venta #{self.venta_id}"
