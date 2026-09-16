from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Prediccion de Precios de Viviendas",
    description="Prediccion de precios de viviendas segun su superficie",
    version="1.0",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models/linear_model.joblib"

model = None
try:
    # Cargar el modelo entrenado
    model = joblib.load(MODEL_PATH)
    print(f"Modelo cargado desde: {MODEL_PATH}")
except Exception as exc:  # noqa: BLE001 - solo registramos el motivo
    print(f"No se pudo cargar el modelo en {MODEL_PATH}: {exc}")
    print("ADVERTENCIA: /predict devolvera 503 hasta que el modelo exista.")


# Esquema de entrada para la prediccion
class housem2(BaseModel):
    area_m2: float = Field(
        ...,
        gt=0,
        description="Superficie de la vivienda en metros cuadrados",
        json_schema_extra={"example": 82.5},
    )


@app.get("/")
def health_check():
    return {
        "status": "OK",
        "message": "API de Prediccion de Precios de Viviendas esta en funcionamiento.",
        "model_loaded": model is not None,
    }


@app.post("/predict")
def predict(data: housem2):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo no disponible. Por favor, intente mas tarde.",
        )

    prediction = model.predict(np.array([[data.area_m2]], dtype=float))[0]

    return {
        "area_m2": data.area_m2,
        "predicted_price": round(float(prediction), 2),
    }
