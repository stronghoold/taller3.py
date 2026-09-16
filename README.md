# Taller 3 - Python y Machine Learning

Proyecto con carga de datos, un modelo de clasificacion (Random Forest) y un
sistema de prediccion de precios de viviendas con API + frontend web.

## Estructura

```
Carga_datos/                          Notebooks de carga de datos (CSV, Excel, API, scraping)
Modelos_ML/RandomForest/              Dataset medico + modelo de clasificacion (Streamlit)
Modelos_ML/RegresionLineal/back/      API de prediccion de precios (FastAPI)
Modelos_ML/RegresionLineal/front/     Frontend web del tasador (Django)
Dockerfile, railway.toml, Procfile    Despliegue del backend en Railway
```

## Backend (FastAPI) - `Modelos_ML/RegresionLineal/back`

```bash
cd Modelos_ML/RegresionLineal/back
pip install -r requirements.txt
python train.py            # genera models/linear_model.joblib
python -m uvicorn main:app --reload
```

| Metodo | Ruta       | Descripcion                                    |
|--------|------------|------------------------------------------------|
| GET    | `/`        | Health check (indica si el modelo esta cargado) |
| POST   | `/predict` | `{"area_m2": 82.5}` -> precio estimado en COP   |

## Frontend (Django) - `Modelos_ML/RegresionLineal/front`

Necesita la API corriendo. La URL se configura con la variable `API_URL`.

```bash
cd Modelos_ML/RegresionLineal/front
pip install -r requirements.txt
python manage.py migrate
API_URL=http://127.0.0.1:8000/predict python manage.py runserver
```

## Despliegue en Railway

Se despliega en **dos servicios** apuntando al mismo repositorio.

### 1. Backend (API)

- Nuevo servicio -> mismo repositorio, **nombre sugerido `backend`**.
- **Settings -> Root Directory**: dejarlo **vacío** (usa la raíz del repo).
- Railway toma `railway.toml` y `Dockerfile` de la raíz, que construyen
  `Modelos_ML/RegresionLineal/back` y entrenan el modelo durante el build.
- **Settings -> Networking -> Generate Domain**: Railway le asigna un dominio
  público, por ejemplo `https://taller3py-backend-production.up.railway.app`.
  Copia ese dominio (sin `/predict`).
- Verifica que quedó arriba abriéndolo en el navegador: debe responder
  `{"status":"OK","model_loaded":true}`. Si `model_loaded` es `false`, el
  modelo no se generó en el build.

### 2. Frontend (Django)

- Nuevo servicio -> mismo repositorio, **nombre sugerido `frontend`**.
- **Settings -> Root Directory**: `Modelos_ML/RegresionLineal/front`
  (Railway leera el `railway.toml` de esa carpeta).
- **Settings -> Networking -> Generate Domain** para tener la URL pública del front.
- Variables -> `API_URL` con el dominio del backend. El front acepta las dos formas
  (si falta el esquema o el `/predict`, los agrega solo):

  ```
  API_URL=https://taller3py-backend-production.up.railway.app
  API_URL=https://taller3py-backend-production.up.railway.app/predict
  ```

  El valor por defecto del código es `http://127.0.0.1:8000/predict` (solo para
  desarrollo local), así que si `API_URL` no está definida en Railway el front
  no llegará a la API.

### 3. Orden recomendado

Despliega primero el **backend**, copia su dominio y recién ahí crea o actualiza
el servicio del **frontend** con la variable `API_URL`; al final vuelve a
desplegar el front para que tome la variable.

### Variables de entorno

| Variable                | Servicio | Obligatoria | Descripcion                                            |
|-------------------------|----------|-------------|--------------------------------------------------------|
| `API_URL`               | frontend | Si          | Dominio del backend, con o sin `/predict`              |
| `PORT`                  | ambos    | No          | La inyecta Railway automaticamente                     |
| `ALLOWED_HOSTS`         | frontend | No          | Por defecto `*`. Ej: `miapp.up.railway.app`            |
| `DJANGO_SECRET_KEY`     | frontend | Recomendada | Clave secreta de Django (usa un valor propio)          |
| `DJANGO_DEBUG`          | frontend | No          | `True` solo para depurar                               |

## Tests

```bash
# Backend
cd Modelos_ML/RegresionLineal/back && python -m pytest test_main.py

# Frontend
cd Modelos_ML/RegresionLineal/front && python manage.py test app_predicc
```

## Problemas comunes

| Sintoma en pantalla                                  | Causa                                                                                          |
|------------------------------------------------------|------------------------------------------------------------------------------------------------|
| `No se pudo conectar con la API (https://...): ...`  | El servicio del backend no existe, está caído o `API_URL` apunta a un dominio viejo (el mensaje muestra la URL usada, revísala). |
| `La API respondió con error 500: Modelo no disponible` | El backend está arriba pero el `linear_model.joblib` no se generó en el build.                  |
| `La API tardó más de 15 segundos en responder`       | El primer request despierta el contenedor; sube `API_TIMEOUT` o revisa los logs del backend.     |
