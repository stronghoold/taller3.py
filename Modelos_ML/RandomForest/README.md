### Sistema de diagnostico clinico con Random Forest

Modelo de clasificacion que predice una de 5 enfermedades (infarto, neumonia,
gripe, ansiedad, gastroenteritis) a partir de 34 variables clinicas.

### Pasos para ejecutar el sistema

Todos los comandos se ejecutan **desde la raiz del repositorio**.

```bash
# 1. Crear entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 2. Instalar librerias
pip install -r Modelos_ML/RandomForest/requirements.txt

# 3. Generar el dataset (5000 registros sinteticos)
python Modelos_ML/RandomForest/1.Crear_dataset.py

# 4. Entrenar el modelo (guarda models/modelo_random_forest_ampliado.pkl)
python Modelos_ML/RandomForest/2.Entrenar_modelo.py

# 5. Ejecutar la app interactiva
streamlit run Modelos_ML/RandomForest/3.Predecir_enfermedad.py
```

### Despliegue (link)
https://modelosml.streamlit.app/
