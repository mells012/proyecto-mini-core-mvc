# Mini Core — Ventas y Comisiones

Proyecto de la asignacion MVC de la semana 4, basado en el ejercicio de
semestres pasados: un "mini core" que **filtra y calcula la comision de
ventas en base a un rango de fechas**, agrupando los resultados por
vendedor y mostrando totales globales del periodo.

- **Backend**: Django + Django REST Framework (patron **MVT**)
- **Frontend**: React + Vite, consumiendo la API via Axios
- **Base de datos**: SQLite (desarrollo); compatible con Postgres en
  produccion via `DATABASE_URL`

---

## El ejercicio

Se modelan tres tablas relacionadas:

1. **Vendedor** — informacion basica de cada vendedor.
2. **ReglaComision** — reglas configurables: a partir de que monto minimo
   de venta se aplica que porcentaje de comision.
3. **Venta** — transacciones de venta, cada una asociada a un vendedor
   (relacion uno a muchos: un vendedor tiene muchas ventas).

Se agrega una cuarta tabla, **ComisionCalculada**, para dejar un historial
(trazabilidad) de cada calculo realizado.

Reglas de comision utilizadas (datos iniciales / "quemados"):

| Regla | Monto minimo | Porcentaje |
|---|---|---|
| Regla basica | $500 | 6% |
| Regla intermedia | $600 | 8% |
| Regla alta | $800 | 10% |
| Regla premium | $1000 | 15% |

La funcionalidad principal: el usuario ingresa un **rango de fechas**, el
sistema filtra las ventas de ese periodo, calcula la comision de cada una
segun la regla que corresponda, y devuelve un reporte agrupado por
vendedor junto con los totales globales.

---

## Por que MVT y no MVC "clasico"

Django no usa el nombre "Controlador", usa su propia variante llamada
**MVT (Modelo - Vista - Template)**, que es equivalente en filosofia de
separacion de responsabilidades al MVC tradicional:

| MVC clasico | Django (MVT) | En este proyecto |
|---|---|---|
| Modelo | **Modelo** (`models.py`) | `ventas/models.py` — define `Vendedor`, `ReglaComision`, `Venta`, `ComisionCalculada` |
| Controlador | **Vista** (`views.py`) | `ventas/views.py` — recibe la peticion HTTP, aplica la logica de negocio (calculo de comisiones) y decide la respuesta |
| Vista | **Template** | En una app Django clasica seria HTML; aqui, al ser una API REST consumida por React, el "template" es el **JSON** que arman los `serializers.py` |

Es decir: lo que en MVC se llama "Controlador" es el **View** de Django, y
lo que en MVC se llama "Vista" (la capa de presentacion) es el
**Template** — en este caso, la respuesta JSON de la API.

---

## Estructura del proyecto

```
proyecto-mvc/
├── backend/                 # Django + DRF
│   ├── config/               # settings, urls, wsgi (configuracion del proyecto)
│   ├── ventas/                # app principal
│   │   ├── models.py            # Modelo (M)
│   │   ├── views.py             # Vista / Controlador (V en MVT = C en MVC)
│   │   ├── serializers.py       # arma el "template" JSON
│   │   ├── urls.py              # rutas de la API
│   │   ├── admin.py             # panel de administracion
│   │   └── management/commands/seed_data.py  # datos iniciales
│   ├── requirements.txt
│   ├── build.sh              # script de build para Render
│   └── manage.py
├── frontend/                 # React + Vite
│   ├── src/
│   │   ├── api/                 # cliente Axios + servicio de la API
│   │   ├── components/          # NavBar
│   │   ├── pages/                # Ventas.jsx (CRUD), Comisiones.jsx (filtro + reporte)
│   │   ├── App.jsx               # rutas (React Router)
│   │   └── index.css
│   └── netlify.toml           # config opcional para desplegar en Netlify
├── render.yaml                # Blueprint de Render (backend + frontend)
└── DEPLOY.md                  # guia paso a paso de despliegue
```

---

## Como correrlo en local

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data      # carga vendedores, reglas y ventas de ejemplo
python manage.py runserver
```

La API queda disponible en `http://127.0.0.1:8000/api/`.

Opcional: crear un superusuario para usar el panel `/admin/`:

```bash
python manage.py createsuperuser
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env            # ya apunta a http://127.0.0.1:8000/api
npm run dev
```

La app queda disponible en `http://127.0.0.1:5173/`.

---

## Endpoints principales de la API

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET | `/api/vendedores/` | Lista de vendedores |
| GET | `/api/reglas/` | Reglas de comision configuradas |
| GET | `/api/ventas/` | Lista de ventas (filtros opcionales: `vendedor`, `fecha_inicio`, `fecha_fin`) |
| POST | `/api/ventas/` | Crear una venta |
| DELETE | `/api/ventas/<id>/` | Eliminar una venta |
| **POST** | **`/api/ventas/calcular-comisiones/`** | **Endpoint clave**: recibe `{"fecha_inicio": "YYYY-MM-DD", "fecha_fin": "YYYY-MM-DD"}` y devuelve el reporte de comisiones agrupado por vendedor + totales globales |
| GET | `/api/comisiones-calculadas/` | Historial de comisiones ya calculadas (trazabilidad) |

---

## Despliegue en la nube

Ver [`DEPLOY.md`](./DEPLOY.md) para la guia completa paso a paso (Render
como opcion principal, con alternativa usando Netlify para el frontend).

- Repositorio: enlaza aqui tu repo de GitHub una vez lo subas.
- Backend desplegado: `https://<tu-backend>.onrender.com`
- Frontend desplegado: `https://<tu-frontend>.onrender.com`

---

## Video explicativo

Ver [`VIDEO_SCRIPT.md`](./VIDEO_SCRIPT.md) para el guion completo de la
explicacion en video (estructura, que mostrar en cada minuto, y el flujo
de demo) y la carpeta `slides/` para las diapositivas de apoyo.
