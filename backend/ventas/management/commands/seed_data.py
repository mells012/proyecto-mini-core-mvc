"""
Comando de gestion para cargar datos iniciales ("datos quemados"):
vendedores, reglas de comision y algunas ventas de ejemplo.

Uso:
    python manage.py seed_data
"""

import datetime
import random

from django.core.management.base import BaseCommand

from ventas.models import ReglaComision, Vendedor, Venta


class Command(BaseCommand):
    help = "Carga datos iniciales de vendedores, reglas de comision y ventas de ejemplo."

    def handle(self, *args, **options):
        self.cargar_vendedores()
        self.cargar_reglas()
        self.cargar_ventas_demo()
        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados correctamente."))

    def cargar_vendedores(self):
        nombres = ["Ana Torres", "Luis Mendoza", "Carla Suarez", "Diego Ramirez"]
        for nombre in nombres:
            Vendedor.objects.get_or_create(
                nombre=nombre, defaults={"email": f"{nombre.split()[0].lower()}@correo.com"}
            )
        self.stdout.write("Vendedores: OK")

    def cargar_reglas(self):
        reglas = [
            {"nombre": "Regla basica", "monto_minimo": 500, "porcentaje": 6},
            {"nombre": "Regla intermedia", "monto_minimo": 600, "porcentaje": 8},
            {"nombre": "Regla alta", "monto_minimo": 800, "porcentaje": 10},
            {"nombre": "Regla premium", "monto_minimo": 1000, "porcentaje": 15},
        ]
        for regla in reglas:
            ReglaComision.objects.get_or_create(
                nombre=regla["nombre"],
                defaults={
                    "monto_minimo": regla["monto_minimo"],
                    "porcentaje": regla["porcentaje"],
                },
            )
        self.stdout.write("Reglas de comision: OK")

    def cargar_ventas_demo(self):
        if Venta.objects.exists():
            self.stdout.write("Ventas de ejemplo: ya existian, se omite.")
            return

        vendedores = list(Vendedor.objects.all())
        montos_posibles = [350, 520, 610, 780, 850, 950, 1050, 1200, 430, 690]
        hoy = datetime.date.today()

        for i in range(10):
            vendedor = random.choice(vendedores)
            monto = random.choice(montos_posibles)
            fecha = hoy - datetime.timedelta(days=random.randint(0, 45))
            Venta.objects.create(
                vendedor=vendedor,
                monto=monto,
                fecha=fecha,
                descripcion=f"Venta de ejemplo #{i + 1}",
            )
        self.stdout.write("Ventas de ejemplo: OK")
