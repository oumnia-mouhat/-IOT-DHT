from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings
from .utils import send_telegram
from rest_framework.renderers import JSONRenderer

# --- API LISTE (GET) ---
@api_view(["GET"])
def Dlist(request):
    all_data = Dht11.objects.all()
    data_ser = DHT11serialize(all_data, many=True)
    return Response(data_ser.data)

# --- API AJOUT (POST) ---
class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize
    renderer_classes = [JSONRenderer]

    def perform_create(self, serializer):
        instance = serializer.save()

        # Email désactivé
        """
        try:
            send_mail(
                subject="⚠️ Alerte Température",
                message=(
                    f"La température a atteint {instance.temp}°C "
                    f"et l'humidité {instance.hum}%\n"
                    f"Horodatage : {instance.dt}"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["stagetessi47@gmail.com"],
                fail_silently=True,
            )
        except Exception:
            pass
        """


        # Telegram actif si temp > 20°C
        # Telegram actif si temp > 20°C
        if instance.temp is not None and instance.temp > 20:
            temp = instance.temp
            hum = instance.hum if instance.hum is not None else "inconnue"
            dt = instance.dt if instance.dt is not None else "inconnue"

            message = f"⚠️ Alerte Température: {temp}°C, Humidité: {hum}%\nHorodatage: {dt}"

            if message.strip():  # vérifie que le message n'est pas vide
                send_telegram(message)

