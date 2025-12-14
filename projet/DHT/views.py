from django.shortcuts import render
from django.http import JsonResponse
from .models import Dht11
from datetime import datetime

def dashboard(request):
    return render(request, "dashboard.html")

def latest_json(request):
    last = Dht11.objects.order_by('-dt').values('temp', 'hum', 'dt').first()
    if not last:
        return JsonResponse({"detail": "no data"}, status=404)
    return JsonResponse({
        "temperature": last["temp"],
        "humidity": last["hum"],
        "timestamp": last["dt"].isoformat()
    })

def api_history(request):
    # Exclut toutes les lignes où temp OU hum est null
    all_data = Dht11.objects.exclude(temp__isnull=True).exclude(hum__isnull=True).order_by('dt').values('temp', 'hum', 'dt')

    data_list = [
        {
            "temperature": d['temp'],
            "humidity": d['hum'],
            "timestamp": d['dt'].isoformat()
        }
        for d in all_data
    ]
    return JsonResponse(data_list, safe=False)


# -------------------- AJOUT POUR L'ESP --------------------
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # pour accepter les requêtes POST de l’ESP sans token CSRF
def post_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            temp = data.get("temp")
            hum = data.get("hum")
            if temp is None or hum is None:
                return JsonResponse({"error": "Missing temp or hum"}, status=400)
            # Création d’un nouvel enregistrement
            Dht11.objects.create(temp=temp, hum=hum, dt=datetime.now())
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "POST method required"}, status=405)
