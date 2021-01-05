from django.urls import path
from .views import VisualizerView, Prueba, BotResponse, AboutUs

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('prueba/', Prueba.as_view()),
    path('aboutUs/', AboutUs.as_view()),
    path('botResults/<int:voting_id>/',BotResponse.as_view()),
]
