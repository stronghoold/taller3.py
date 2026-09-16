from pathlib import Path
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# predecir precios de viviendas segun la superficie en M2

# datos de entrenamiento (x) y etiquetas (y)
x = np.array([[40], [50], [60], [85], [100], [150]])
y = np.array([10000000, 12000000, 15000000, 20000000, 25000000, 30000000])

# entrenar el modelo de regresion lineal
model = LinearRegression()
model.fit(x, y)

# predicciones de prueba
y_pred = model.predict(x)

# imprimir la informacion del modelo entrenado
print("Coeficiente de regression: ", model.coef_[0])
print("Termino independiente: ", model.intercept_)

# graficar datos reales
plt.scatter(x, y, color='red', label='Datos reales')

# graficar la linea de regresion
plt.plot(x, y_pred, color='blue', label='Línea de regresión')

plt.xlabel('Superficie (m2)')
plt.ylabel('Precio (COP)')
plt.title('Regresión Lineal: Precio de Viviendas segun Superficie (m2)')
plt.legend()
plt.grid(True)

# imprimir
plt.show()

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models/linear_model.joblib"

# crear la carpeta "models" si no existe
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

# guardar el modelo entrenado en un archivo
joblib.dump(model, MODEL_PATH)