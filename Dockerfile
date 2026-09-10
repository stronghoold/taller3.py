FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Entrena y genera el modelo durante el build
RUN python train.py

ENV PORT=8000
EXPOSE ${PORT}

CMD python -m uvicorn main:app --host 0.0.0.0 --port ${PORT}
