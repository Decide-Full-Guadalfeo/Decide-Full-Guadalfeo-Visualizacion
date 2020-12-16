from django.urls import path
from .views import VisualizerView, Prueba


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('prueba/', Prueba.as_view()),
   
]
