# 🐍 Taller 3 — Python & Machine Learning

Proyecto de práctica que cubre dos etapas de un flujo de Machine Learning:

1. **Carga de datos** con Pandas desde distintas fuentes (CSV, Excel, API y web scraping).
2. **Modelo de clasificación** con Random Forest para diagnóstico clínico de 5 enfermedades, incluyendo una app web en Streamlit.

---

## 📁 Estructura del proyecto

```
taller3_pyml/
├── Carga_datos/                         # Notebooks: cargar datos desde distintas fuentes
│   ├── 1.csv_carga_datos.ipynb          #   CSV + tareas de preprocesamiento
│   ├── 2.excel_carga_datos.ipynb        #   Excel (.xlsx con openpyxl)
│   ├── 3.api_carga_datos.ipynb          #   API REST (Rick & Morty)
│   ├── 4.webscraping_carga_datos.ipynb  #   Web scraping (Wikipedia con pd.read_html)
│   ├── dataset_ventas.csv               #   Dataset de ventas (CSV)
│   └── dataset_ventas.xlsx              #   Dataset de ventas (Excel)
│
├── Modelos_ML/
│   └── RandomForest/
│       ├── 1.Crear_dataset.py           # Genera dataset médico sintético (5000 registros)
│       ├── 2.Entrenar_modelo.py         # Entrena y guarda el Random Forest
│       ├── 3.Predecir_enfermedad.py     # App Streamlit de diagnóstico clínico
│       ├── data/                        # dataset_medico_ampliado.csv
│       └── models/                      # modelo_random_forest_ampliado.pkl
│
├── data/                                # Copia del dataset (raíz)
├── models/                              # Copia del modelo (raíz)
├── requirements.txt
└── README.md
```

---

## 🚀 Instalación

Requiere **Python 3.10+**.

```bash
# 1. Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

---

## 📓 1. Carga de datos (notebooks)

Abre los notebooks desde la carpeta `Carga_datos/`:

```bash
jupyter notebook
# o
jupyter lab
```

El notebook `1.csv_carga_datos.ipynb` además incluye las **5 tareas de preprocesamiento** sobre `dataset_ventas.csv`:

| # | Tarea | Herramienta |
|---|-------|-------------|
| 1 | Manejo de valores faltantes y duplicados | `isnull()`, `dropna()`, `duplicated()` |
| 2 | Codificación de variables categóricas | `LabelEncoder` y One-Hot (`pd.get_dummies`) |
| 3 | Normalización y estandarización | `MinMaxScaler` y `StandardScaler` |
| 4 | Balanceo de la variable objetivo | `SMOTE` (requiere `imbalanced-learn`) |
| 5 | Dataset final listo para entrenar | DataFrame balanceado |

> ⚠️ La tarea 4 necesita `imbalanced-learn`, incluida en `requirements.txt`.

---

## 🤖 2. Modelo Random Forest (diagnóstico clínico)

El pipeline entrena un clasificador que detecta 5 enfermedades a partir de **34 variables clínicas** (signos vitales, factores de riesgo y síntomas): `infarto`, `neumonia`, `gripe`, `ansiedad` y `gastroenteritis`.

Ejecuta los scripts **desde la carpeta** `Modelos_ML/RandomForest/` (usan rutas relativas):

```bash
cd Modelos_ML/RandomForest

# Paso 1: generar el dataset sintético (5000 registros)
python 1.Crear_dataset.py

# Paso 2: entrenar el modelo y guardarlo en models/modelo_random_forest_ampliado.pkl
python 2.Entrenar_modelo.py

# Paso 3: lanzar la app web de diagnóstico
streamlit run 3.Predecir_enfermedad.py
```

La app abre en el navegador (por defecto `http://localhost:8501`). Rellena signos vitales, factores de riesgo y síntomas en las 4 pestañas, pulsa **"🔍 Realizar Diagnóstico Integral"** y obtendrás:

- Enfermedad predicha con su nivel de urgencia y confianza.
- Probabilidades de las 5 clases en un gráfico de barras.
- Recomendación clínica asociada.

> ⚠️ Herramienta educativa de apoyo. El diagnóstico definitivo siempre corresponde a un profesional de la salud.

---

## 🔧 Solución de problemas

- **`imbalanced-learn` no encontrado** → `pip install -r requirements.txt` o `pip install imbalanced-learn`.
- **Warning de versión al cargar el `.pkl`** → el modelo fue entrenado con otra versión de scikit-learn. Funciona igual; para eliminarlo reentrena con `python 2.Entrenar_modelo.py`.
- **`ModuleNotFoundError: streamlit / plotly`** → `pip install streamlit plotly` (ya están en `requirements.txt`).
- **Error al leer el Excel** → `pip install openpyxl`.