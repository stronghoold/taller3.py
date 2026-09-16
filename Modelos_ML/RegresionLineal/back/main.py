from pathlib import Path
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Prediccion de Precios de Viviendas",
    description="Prediccion de precios de viviendas segun su superficie",
    version="1.0"
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models/linear_model.joblib"

try:
    # cargar el modelo entrenado
    model = joblib.load(MODEL_PATH)
except Exception:
    model = None

class HouseM2(BaseModel):
    area_m2: float = Field(..., example=82.5, description="Superficie de la vivienda en metros cuadrados", gt=0)

@app.get("/")
def health_check():
    return {"status": "OK", "message": "API de Prediccion de Precios de Viviendas esta en funcionamiento.", "model_loaded": model is not None}

@app.post("/predict")
def predict_price(data: HouseM2):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible. Intente nuevamente más tarde.")

    prediction = model.predict([[data.area_m2]])
    predicted_price = round(float(prediction[0]), 2)

    return {"area_m2": data.area_m2, "predicted_price": predicted_price}