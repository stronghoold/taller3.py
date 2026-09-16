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

- Sin *Root Directory* (usa la raiz del repo).
- Railway toma `railway.toml` y `Dockerfile` de la raiz, que construyen
  `Modelos_ML/RegresionLineal/back` y entrenan el modelo durante el build.
- Copia el dominio publico que le asigne Railway, por ejemplo
  `https://mi-backend.up.railway.app`.

### 2. Frontend (Django)

- Nuevo servicio -> mismo repositorio.
- **Settings -> Root Directory**: `Modelos_ML/RegresionLineal/front`
  (Railway leera el `railway.toml` de esa carpeta).
- Variable de entorno obligatoria:
  `API_URL=https://mi-backend.up.railway.app/predict`

### Variables de entorno

| Variable                | Servicio | Obligatoria | Descripcion                                            |
|-------------------------|----------|-------------|--------------------------------------------------------|
| `API_URL`               | frontend | Si          | URL completa del endpoint `/predict` del backend       |
| `PORT`                  | ambos    | No          | La inyecta Railway automaticamente                     |
| `ALLOWED_HOSTS`         | frontend | No          | Por defecto `*`. Ej: `miapp.up.railway.app`            |
| `DJANGO_SECRET_KEY`     | frontend | Recomendada | Clave secreta de Django (usa un valor propio)          |
| `DJANGO_DEBUG`          | frontend | No          | `True` solo para depurar                               |

## Tests

```bash
# Backend
cd Modelos_ML/RegresionLineal/back && python -m pytest test_main.py

# Frontend
cd Modelos_ML/RegresionLineal/front && python manage.py test app_prediccion
```
