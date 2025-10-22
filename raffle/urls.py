from django.urls import path
from . import views

urlpatterns = [
    path('', views.raffle_list, name='raffle_list'),
    path('sorteo/<int:raffle_id>/', views.raffle_detail, name='raffle_detail'),
    path('top-jugadores/', views.top_participants, name='top_participants'),
    path("historial-de-ganadores-diarios/", views.daily_winners_history, name="daily_winners_history"),
]
