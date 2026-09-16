FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    PORT=8000

WORKDIR /app

# Unica fuente de verdad del backend: Modelos_ML/RegresionLineal/back
COPY Modelos_ML/RegresionLineal/back/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY Modelos_ML/RegresionLineal/back/ .

# Entrena y genera el artefacto durante el build
RUN python train.py

EXPOSE 8000

# 'sh -c' es necesario para que ${PORT} (inyectado por Railway) se expanda
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
