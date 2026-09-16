import os
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# El decorador @csrf_exempt apaga la validación de seguridad para este formulario
@csrf_exempt
def home(request):
    context = {}
    if request.method == 'POST':
        area_m2 = request.POST.get('area_m2')
        if area_m2:
            try:
                area_m2 = float(area_m2)
                if area_m2 <= 0:
                    context['error'] = 'La superficie debe ser mayor a 0 m².'
                    return render(request, 'index.html', context)
            except ValueError:
                context['error'] = 'El valor ingresado no es válido.'
                return render(request, 'index.html', context)

            try:
                # Usa la variable de entorno de Railway, o la URL del backend si estás en tu PC
                api_url = os.environ.get(
                    "API_URL",
                    "https://bloback.up.railway.app/predict"
                )
                payload = {"area_m2": area_m2}

                response = requests.post(api_url, json=payload, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    # Formato colombiano: $194.506 (punto como separador de miles)
                    precio = round(data['predicted_price'])
                    precio_formateado = f"${precio:,}".replace(",", ".")
                    context['resultado'] = precio_formateado
                    context['area'] = area_m2
                else:
                    context['error'] = f"Error del servidor: {response.status_code}"

            except requests.exceptions.ConnectionError:
                context['error'] = 'No se pudo conectar con el servidor de predicción.'
            except requests.exceptions.Timeout:
                context['error'] = 'El servidor tardó demasiado en responder.'
            except requests.exceptions.RequestException:
                context['error'] = "No se pudo conectar con la API."

    return render(request, 'index.html', context)
