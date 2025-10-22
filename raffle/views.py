from django.shortcuts import render, get_object_or_404
from .models import Raffle, RaffleNumber
from django.db.models import Count
from .models import Participant, DailyWinner
from django.utils import timezone
import random
from datetime import date


START_DATE = date(2025, 11, 1)

def raffle_list(request):
    """Muestra todos los sorteos."""
    daily_winner = get_or_create_daily_winner()
    raffles = Raffle.objects.all().order_by('-created_at')
    context = {
        'raffles': raffles,
        'daily_winner': daily_winner,
    }
    return render(request, 'index.html', context)

def raffle_detail(request, raffle_id):
    """Muestra información de un sorteo."""

    raffle = get_object_or_404(Raffle, pk=raffle_id)
    assigned_numbers = RaffleNumber.objects.filter(raffle=raffle).select_related('participant')
    taken_numbers = [n.number for n in assigned_numbers]
    available_numbers = [n for n in range(100) if n not in taken_numbers]

    context = {
        'raffle': raffle,
        'assigned_numbers': assigned_numbers,
        'available_numbers': available_numbers,
    }

    return render(request, 'raffle_detail.html', context)

def top_participants(request):
    """
    Muestra los participantes más activos de todos los sorteos,
    ordenados por la cantidad de números que han registrado.
    """
    participants = Participant.objects.annotate(
        total_numbers=Count('numbers')
    ).order_by('-total_numbers')  # De mayor a menor

    context = {
        'participants': participants
    }
    return render(request, 'top_participants.html', context)

def get_or_create_daily_winner():
    """
    Retorna el ganador del día. Si no existe, selecciona uno aleatorio y lo registra.
    """
    today = timezone.localdate()  # Fecha del día según zona horaria
    if today < START_DATE:
        return None

    winner, created = DailyWinner.objects.get_or_create(date=today, defaults={
        'participant': random.choice(Participant.objects.all())
    })

    return winner

def daily_winners_history(request):
    """
    Muestra el historial de ganadores diarios, del más reciente al más antiguo.
    """
    get_or_create_daily_winner()
    winners = DailyWinner.objects.select_related('participant').order_by('-date')

    context = {
        'winners': winners
    }
    return render(request, 'daily_winners_history.html', context)