# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Dht11
from .utils import send_telegram
from datetime import datetime
import threading
import time

def alert_temp_with_reminder(temp, hum=None):
    """
    Envoie une alerte Telegram immédiate puis un rappel toutes les 10 minutes.
    Affiche date et heure système.
    """
    start_time = datetime.now()
    hum_text = f"{hum}%" if hum is not None else "inconnue"
    current_time = start_time.strftime('%d/%m/%Y %H:%M:%S')  # date + heure système

    # Message initial
    send_telegram(
        f"🌡️⚠️ Alerte Température ⚠️🌡️\n\n"
        f"Température: {temp}°C\n"
        f"Humidité: {hum_text}\n"
        f"Horodatage: {current_time}"
    )

    # Fonction rappel toutes les 10 minutes
    def reminder_loop():
        while True:
            time.sleep(600)  # 10 min
            elapsed = datetime.now() - start_time
            hours, remainder = divmod(elapsed.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            send_telegram(
                f"⏱ Rappel Température ⏱\n\n"
                f"Température: {temp}°C\n"
                f"Humidité: {hum_text}\n"
                f"Heure actuelle: {current_time}\n"
                f"Durée écoulée: {int(hours)}h {int(minutes)}m"
            )

    threading.Thread(target=reminder_loop, daemon=True).start()


# Exemple statique pour test
temp = 23
hum = 60
if temp > 20:
    alert_temp_with_reminder(temp, hum)


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
