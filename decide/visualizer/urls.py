from django.urls import path
from .views import VisualizerView, Prueba
from visualizer import views

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('prueba/', Prueba.as_view()),
    path('botResults/',views.botResponse),
]
