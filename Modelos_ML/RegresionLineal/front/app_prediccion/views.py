import os

import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Endpoint del backend FastAPI. En Railway se configura con la variable API_URL.
DEFAULT_API_URL = "http://127.0.0.1:8000/predict"


# El decorador @csrf_exempt apaga la validacion de CSRF para este formulario:
# es publico, no hay autenticacion y no modifica estado, solo consulta la API.
@csrf_exempt
def home(request):
    context = {}

    if request.method == "POST":
        area_m2 = request.POST.get("area_m2")

        if not area_m2:
            context["error"] = "Debes ingresar el área de la vivienda."
            return render(request, "index.html", context)

        try:
            payload = {"area_m2": float(area_m2)}
        except (TypeError, ValueError):
            context["error"] = "El área debe ser un número válido (ej: 85.5)."
            return render(request, "index.html", context)

        api_url = os.environ.get("API_URL", DEFAULT_API_URL)

        try:
            response = requests.post(api_url, json=payload, timeout=10)
        except requests.exceptions.RequestException:
            context["error"] = "No se pudo conectar con la API."
            return render(request, "index.html", context)

        if response.status_code == 200:
            try:
                precio = float(response.json()["predicted_price"])
            except (ValueError, KeyError, TypeError):
                context["error"] = "La API devolvió una respuesta inesperada."
                return render(request, "index.html", context)

            context["resultado"] = f"${precio:,.2f}"
            context["area"] = area_m2
        else:
            context["error"] = (
                f"La API respondió con un error (código {response.status_code})."
            )

    return render(request, "index.html", context)
