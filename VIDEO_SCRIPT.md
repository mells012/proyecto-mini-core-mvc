# Guion del video explicativo — Mini Core: Ventas y Comisiones

Duracion estimada: 9-11 minutos. Estructura inspirada en la presentacion
de referencia de semestres pasados (stack, patron MVT, modelos, logica de
negocio, frontend y despliegue), aplicada a este proyecto propio.

Antes de grabar: ten abiertos (1) el editor con el proyecto, (2) el
backend corriendo en local o el admin de Django, (3) el frontend
desplegado en la nube, y (4) este guion o las diapositivas como apoyo.

---

## 1. Introduccion (0:00 - 0:45)

> "Hola, buenas [tardes/dias]. Mi nombre es [tu nombre] y en este video voy
> a presentar mi proyecto Mini Core, desarrollado en funcion del ejercicio
> de Ingenieria Web sobre el patron MVC, replicando la logica de un
> ejercicio de semestres pasados: un sistema que filtra y calcula
> comisiones de ventas en base a un rango de fechas.
>
> Voy a explicar el stack tecnologico utilizado, como se aplica el patron
> MVC —o su equivalente en Django, MVT— tanto en el backend como en el
> frontend, la logica de negocio central del proyecto, y finalmente como
> se realizo el despliegue en la nube."

**Mostrar en pantalla:** portada / diapositiva de titulo.

---

## 2. Stack tecnologico (0:45 - 1:30)

> "El stack que utilice es: para el backend, Django con Django REST
> Framework, usando Python; y para el frontend, React con Vite,
> consumiendo la API mediante Axios. La base de datos utilizada es SQLite
> por simplicidad, aunque el proyecto esta preparado para migrar a
> Postgres en produccion mediante una variable de entorno."

**Mostrar en pantalla:** diapositiva de stack tecnologico, o el
`requirements.txt` y `package.json`.

---

## 3. El patron MVC y su equivalente MVT en Django (1:30 - 3:00)

> "Como ya sabemos, el desarrollo sigue el patron MVC: Modelo, Vista y
> Controlador. Sin embargo, Django utiliza una adaptacion llamada MVT:
> Modelo, Vista y Template, que es equivalente en cuanto a la filosofia de
> separacion de responsabilidades.
>
> El Modelo se mantiene igual: representa la estructura de datos, las
> clases, campos y relaciones.
>
> Lo que en MVC llamamos Controlador, en Django se llama View: recibe la
> peticion HTTP, aplica la logica de negocio, y decide que respuesta
> devolver.
>
> Y lo que en MVC es la Vista —la capa de presentacion— en Django se llama
> Template. En mi caso, como el frontend esta separado en React y el
> backend funciona como una API REST, el 'template' que genera Django no
> es HTML sino JSON, estructurado mediante los serializers de Django REST
> Framework."

**Mostrar en pantalla:** diapositiva con la tabla comparativa MVC vs MVT
(incluida en las slides).

---

## 4. Estructura del proyecto (3:00 - 3:45)

> "Para organizar el desarrollo, separe el proyecto en dos carpetas: una
> para el backend, con Django y Python; y otra para el frontend, con
> JavaScript y React. Dentro del backend tengo la app 'ventas', que
> concentra los modelos, vistas, serializers y rutas de la API."

**Mostrar en pantalla:** arbol de carpetas en el editor (`backend/` y
`frontend/`).

---

## 5. Configuracion (settings.py) (3:45 - 4:30)

> "En la configuracion del proyecto, registre mi aplicacion 'ventas' como
> app instalada, junto con las dependencias de terceros: Django REST
> Framework para construir la API, y Cors Headers para permitir la
> comunicacion entre el backend y el frontend, que corren en puertos o
> dominios distintos.
>
> Tambien configure White Noise para la gestion de archivos estaticos en
> produccion, y defini la SECRET_KEY, el modo DEBUG y los ALLOWED_HOSTS a
> traves de variables de entorno, para diferenciar el comportamiento entre
> desarrollo y produccion. La base de datos utilizada por defecto es
> SQLite, pensada para simplificar el desarrollo."

**Mostrar en pantalla:** `backend/config/settings.py`.

---

## 6. El ejercicio: modelos (4:30 - 6:00)

> "El ejercicio consiste en tres tablas relacionadas: Vendedor, Venta y
> ReglaComision. El modelo Vendedor almacena la informacion basica de cada
> vendedor, con validacion de nombre unico.
>
> El modelo ReglaComision define las reglas configurables de comision: a
> partir de que monto minimo de venta se aplica que porcentaje. Por
> ejemplo, ventas desde 500 dolares aplican 6%, desde 600 aplican 8%,
> desde 800 aplican 10%, y desde 1000 aplican 15%.
>
> El modelo Venta registra cada transaccion, con una relacion uno a
> muchos hacia Vendedor: un vendedor puede tener muchas ventas.
>
> Finalmente, agregue un cuarto modelo, ComisionCalculada, que no estaba
> en el enunciado original pero que agrega trazabilidad: guarda un
> historial de cada calculo de comision realizado."

**Mostrar en pantalla:** `backend/ventas/models.py`.

---

## 7. Logica de negocio: calculo de comisiones (6:00 - 7:30)

> "La funcionalidad principal del Mini Core es el endpoint
> 'calcular-comisiones', al que se le envia un rango de fechas. Ahi es
> donde esta el nucleo de la logica de negocio.
>
> Primero se valida que el rango de fechas sea correcto. Luego se filtran
> las ventas que caen dentro de ese periodo. Para cada venta, se busca la
> regla de comision con el monto minimo mas alto que la venta SI alcanza
> a cubrir, y se calcula el monto de la comision.
>
> Cada calculo se guarda en el historial de ComisionCalculada. Finalmente,
> se arma un reporte estructurado: un resumen agrupado por vendedor, con
> el total vendido y el total de comision de cada uno, mas el detalle
> individual de cada venta, y tambien los totales globales del periodo."

**Mostrar en pantalla:** `backend/ventas/views.py`, metodo
`calcular_comisiones`. Opcional: probar el endpoint con una herramienta
como el navegador, curl o Postman mientras se explica.

---

## 8. Serializers (7:30 - 8:00)

> "Los serializers son los que arman la respuesta JSON que consume el
> frontend. Ahi tambien incluyo validaciones, como que el monto de una
> venta no puede ser menor o igual a cero, o que la fecha de inicio no
> puede ser posterior a la fecha de fin."

**Mostrar en pantalla:** `backend/ventas/serializers.py`.

---

## 9. Frontend: estructura y funcionalidad (8:00 - 9:00)

> "En el frontend, organice el proyecto en carpetas: 'api' para la
> conexion con el backend mediante Axios, 'components' para elementos
> compartidos como la barra de navegacion, y 'pages' para las dos
> pantallas principales.
>
> La pagina de Ventas permite el CRUD de ventas: agregar una nueva venta
> seleccionando el vendedor, el monto y la fecha; ver el listado completo
> con la comision estimada calculada automaticamente; y eliminar ventas.
>
> La pagina de Comisiones permite seleccionar un rango de fechas y
> ejecutar el calculo, mostrando el resumen por vendedor y los totales
> globales del periodo."

**Mostrar en pantalla:** `frontend/src/pages/Ventas.jsx` y
`Comisiones.jsx` brevemente, o directamente pasar a la demo en vivo.

---

## 10. Demo en vivo (9:00 - 10:30)

> "Vamos a ver el proyecto funcionando, ya desplegado en la nube."

**Acciones a realizar en pantalla (sobre el sitio desplegado):**
1. Abrir la URL del frontend desplegado.
2. En la pagina de Ventas: mostrar el listado de ventas ya cargado
   (datos iniciales), con su comision estimada.
3. Agregar una venta nueva (elegir vendedor, monto, fecha) y mostrar que
   aparece en el listado con su comision calculada.
4. Ir a la pagina de Comisiones, seleccionar un rango de fechas, y
   presionar "Calcular comisiones".
5. Mostrar el resumen: cantidad de vendedores, cantidad de ventas, total
   vendido y total de comisiones del periodo.
6. Mostrar el detalle agrupado por vendedor, señalando un caso en el que
   una venta no alcanza el monto minimo de ninguna regla (por lo tanto no
   genera comision).
7. Cambiar el rango de fechas y volver a calcular, para mostrar que el
   resultado cambia dinamicamente.

> "Como pueden ver, el calculo se actualiza en funcion del rango de
> fechas seleccionado, agrupando por vendedor y mostrando el total global
> del periodo."

---

## 11. Despliegue (10:30 - 11:15)

> "Para el despliegue, utilice Render: un Web Service para el backend de
> Django, y un Static Site para el frontend de React. El backend expone
> la API en su propia URL, y el frontend, ya compilado, consume esa API
> mediante una variable de entorno que indica la URL base.
>
> Tambien deje documentada una alternativa usando Netlify para el
> frontend, mantiniendo el backend en Render, ya que Netlify no soporta
> backends con estado como Django."

**Mostrar en pantalla:** diapositiva con el diagrama de despliegue, o el
dashboard de Render mostrando ambos servicios activos.

---

## 12. Cierre (11:15 - 11:30)

> "En resumen, el proyecto aplica el patron MVC —adaptado como MVT en
> Django— separando claramente el modelo de datos, la logica de negocio
> en las vistas, y la presentacion en los serializers y en el frontend de
> React. La funcionalidad central, el calculo de comisiones por rango de
> fechas agrupado por vendedor, queda disponible tanto en local como
> desplegada en la nube.
>
> Muchas gracias por su atencion."

**Mostrar en pantalla:** diapositiva final con los links del repositorio
y del despliegue.

---

## Checklist rapido antes de grabar

- [ ] Backend desplegado y accesible (probar la URL antes de grabar)
- [ ] Frontend desplegado y accesible
- [ ] Datos de ejemplo cargados (`seed_data`) para que la demo no empiece vacia
- [ ] Repositorio en GitHub actualizado y publico (o con acceso dado al docente)
- [ ] Pantalla y audio probados antes de grabar la version final
