from django.urls import path
from django.views.generic import TemplateView  # Ici ça fonctionne parce que views.py est dans DHT
from DHT import views
urlpatterns = [
    # Dashboard principal
    path('', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),

    # Pages graphiques
    path('graph_temp/', TemplateView.as_view(template_name="graph_temp.html"), name='graph_temp'),
    path('graph_hum/', TemplateView.as_view(template_name="graph_hum.html"), name='graph_hum'),

    # API pour la dernière mesure
    path('latest/', views.latest_json, name='latest'),

    # API pour l'historique (Chart.js)
    path('api/', views.api_history, name='api_history'),
    path('api/post', views.post_data, name='post_data'),
]
