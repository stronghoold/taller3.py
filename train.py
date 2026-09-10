import joblib
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression

#predecir precios de viviendas segun la superficie en M2

#datos de entrenamiento (x) y etiquetas (y)

x = np.array([[40], [50], [60], [85], [100], [150]])

y = np.array([100000, 120000, 150000, 200000, 250000, 300000]) 

#entrenar el modelo de regresion lineal

model = LinearRegression()
model.fit(x, y)

#imprimir la informacion del modelo entrenado
print("Coeficiente de regression: ", model.coef_[0])
print("Termino independiente: ", model.intercept_)

#guardar el modelo entrenado en un archivo
model_dir = Path('Modelos_ML/RegresionLineal/models')
model_dir.mkdir(parents=True, exist_ok=True)
joblib.dump(model, model_dir / 'linear_model.joblib')
print("Modelo guardado en:", model_dir / 'linear_model.joblib')