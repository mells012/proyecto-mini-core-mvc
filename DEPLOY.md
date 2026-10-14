# Guia de despliegue

Este proyecto se compone de dos partes independientes que se despliegan por
separado:

- **Backend**: Django + Django REST Framework → se despliega como
  **Web Service** (necesita un proceso corriendo, no es un sitio estatico).
- **Frontend**: React + Vite → se despliega como **Static Site** (genera
  archivos HTML/CSS/JS estaticos).

A continuacion, dos rutas posibles. La **Opcion A (Render)** replica lo que
se explica en el video de referencia (un Web Service + un Static Site en la
misma plataforma). La **Opcion B** usa Netlify solo para el frontend
(Netlify no ejecuta backends Django), dejando el backend en Render.

---

## Opcion A: Todo en Render (recomendada)

### 1. Subir el proyecto a GitHub

```bash
git init
git add .
git commit -m "Proyecto Mini Core - Ventas y Comisiones"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/<tu-repo>.git
git push -u origin main
```

### 2. Desplegar usando el Blueprint (`render.yaml`)

El repositorio incluye un archivo `render.yaml` en la raiz que define ambos
servicios (backend + frontend) listos para desplegarse juntos:

1. Entra a [render.com](https://render.com) e inicia sesion.
2. Click en **New > Blueprint**.
3. Conecta tu repositorio de GitHub.
4. Render detecta `render.yaml` y muestra los dos servicios a crear:
   `mini-core-backend` (Web Service) y `mini-core-frontend` (Static Site).
5. Click en **Apply**. Render construira y desplegara ambos servicios.
6. Una vez desplegado el backend, copia su URL (algo como
   `https://mini-core-backend.onrender.com`) y actualiza la variable de
   entorno `VITE_API_URL` del servicio frontend si no coincide
   automaticamente, apuntando a `https://mini-core-backend.onrender.com/api`.
7. Actualiza tambien `CORS_ALLOWED_ORIGINS` en el backend con la URL real
   del frontend desplegado, y `ALLOWED_HOSTS` con el dominio real del
   backend, si Render les asigna nombres distintos a los sugeridos.

### 2-bis. Alternativa: crear los servicios manualmente (sin Blueprint)

Si prefieres crearlos a mano, como se muestra en el video de referencia:

**Backend (Web Service):**
1. **New > Web Service** → conecta el repo → **Root Directory**: `backend`
2. **Build Command**: `./build.sh`
3. **Start Command**: `gunicorn config.wsgi:application`
4. Variables de entorno:
   - `SECRET_KEY`: genera un valor aleatorio
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: el dominio que Render te asigne (ej. `mini-core-backend.onrender.com`)
   - `CORS_ALLOWED_ORIGINS`: la URL del frontend (la agregas despues de crearlo)

**Frontend (Static Site):**
1. **New > Static Site** → conecta el repo → **Root Directory**: `frontend`
2. **Build Command**: `npm install && npm run build`
3. **Publish Directory**: `dist`
4. Variable de entorno: `VITE_API_URL` = `https://<tu-backend>.onrender.com/api`
5. En **Redirects/Rewrites** agrega: origen `/*` → destino `/index.html` (para que funcionen las rutas de React Router)

### 3. Verificar

- Backend: abre `https://<tu-backend>.onrender.com/` → deberia responder un JSON `{"status": "ok", ...}`
- Frontend: abre `https://<tu-frontend>.onrender.com/` → deberia cargar la app y listar ventas

> Nota: en el plan gratuito de Render los servicios "duermen" tras un rato
> de inactividad: la primera peticion despues de dormir puede tardar unos
> segundos en responder mientras el servicio arranca de nuevo.

---

## Opcion B: Frontend en Netlify + Backend en Render

El backend de Django **no puede alojarse en Netlify** (solo sirve sitios
estaticos), asi que en esta opcion el backend sigue yendo a Render
(seguir los pasos de "Backend" de la Opcion A) y solo el frontend cambia:

1. Entra a [netlify.com](https://netlify.com) e inicia sesion.
2. **Add new site > Import an existing project** → conecta GitHub → selecciona el repo.
3. **Base directory**: `frontend`
4. **Build command**: `npm run build`
5. **Publish directory**: `frontend/dist`
6. En **Site settings > Environment variables** agrega:
   - `VITE_API_URL` = `https://<tu-backend>.onrender.com/api`
7. Despliega. El archivo `frontend/netlify.toml` ya incluye la
   configuracion de build y el redirect necesario para que las rutas de
   React Router funcionen correctamente.
8. Vuelve al backend en Render y agrega la URL de Netlify
   (ej. `https://tu-sitio.netlify.app`) a la variable `CORS_ALLOWED_ORIGINS`.

---

## Resumen de variables de entorno

### Backend
| Variable | Descripcion | Ejemplo |
|---|---|---|
| `SECRET_KEY` | Clave secreta de Django | valor aleatorio generado por Render |
| `DEBUG` | Modo debug | `False` en produccion |
| `ALLOWED_HOSTS` | Dominios permitidos, separados por coma | `mini-core-backend.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | Origenes del frontend permitidos, separados por coma | `https://mini-core-frontend.onrender.com` |
| `DATABASE_URL` | (Opcional) URL de una base Postgres si se quiere migrar de SQLite | `postgres://...` |

### Frontend
| Variable | Descripcion | Ejemplo |
|---|---|---|
| `VITE_API_URL` | URL base de la API del backend | `https://mini-core-backend.onrender.com/api` |
