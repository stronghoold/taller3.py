import joblib
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression

# Predecir precios de viviendas segun la superficie en m2

# Datos de entrenamiento (X) y etiquetas (y)
x = np.array([[40], [50], [60], [90], [100], [120]])
y = np.array([210000000, 300000000, 350000000, 500000000, 600000000, 700000000])

# Entrenar el modelo de regresion lineal
model = LinearRegression()
model.fit(x, y)

# Predicciones de prueba
y_pred = model.predict(x)

# Imprimir la informacion del modelo entrenado
print("Coeficiente de regresion:", model.coef_[0])
print("Termino independiente:", model.intercept_)

# Graficar datos reales (requiere matplotlib y un backend sin pantalla: MPLBACKEND=Agg)
# plt.scatter(x, y, color='red', label='Datos de entrenamiento')
# plt.plot(x, y_pred, color='blue', label='Linea de regresion')
# plt.xlabel('Superficie (m2)')
# plt.ylabel('Precio (COP)')
# plt.title('Regresion Lineal: Precio de Viviendas segun Superficie (m2)')
# plt.legend()
# plt.grid(True)
# plt.show()

# Guardar el artefacto del modelo entrenado en un archivo
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "linear_model.joblib"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)
print("Modelo guardado en:", MODEL_PATH)
