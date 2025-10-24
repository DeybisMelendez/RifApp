from django.shortcuts import render, get_object_or_404,redirect
from .models import Raffle, RaffleNumber
from django.db.models import Count
from .models import Participant, DailyWinner
from django.utils import timezone
import random
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ParticipantForm, RaffleNumberForm
from django.contrib import messages

START_DATE = date(2025, 11, 1)
END_DATE = date(2025, 12, 24)

def raffle_list(request):
    """Muestra todos los sorteos."""
    daily_winner = get_or_create_daily_winner()
    run_mass_draw()
    raffles = Raffle.objects.all().order_by('-created_at')
    context = {
        'raffles': raffles,
        'daily_winner': daily_winner,
    }
    return render(request, 'index.html', context)

def raffle_detail(request, raffle_id):
    """Muestra información de un sorteo."""

    raffle = get_object_or_404(Raffle, pk=raffle_id)
    winner = None
    if raffle.finalized:
        winner = RaffleNumber.objects.get(raffle=raffle, number=raffle.number_winner)
    assigned_numbers = RaffleNumber.objects.filter(raffle=raffle).select_related('participant')
    taken_numbers = [n.number for n in assigned_numbers]
    available_numbers = [n for n in range(100) if n not in taken_numbers]

    context = {
        'raffle': raffle,
        'assigned_numbers': assigned_numbers,
        'available_numbers': available_numbers,
        'winner': winner,
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

def run_mass_draw():
    """
    Realiza un sorteo para todos los sorteos disponibles (finalized=False)
    en la fecha 24 de diciembre de 2025. 
    Asegura que ningún participante gane más de una vez.
    """
    today = date.today()

    if today != END_DATE:
        return

    raffles = Raffle.objects.filter(finalized=False)

    for raffle in raffles:
        available_numbers = RaffleNumber.objects.filter(raffle=raffle)

        winner_number = random.choice(available_numbers)
        raffle.number_winner = winner_number.number
        raffle.finalized = True
        raffle.save()

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


@staff_member_required
def add_participant(request):
    """Vista para crear un nuevo participante (solo administradores)."""
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f"Participante '{participant.name}' agregado correctamente.")
            return redirect('add_participant')
        else:
            messages.error(request, "Ocurrió un error al guardar el participante. Verifica los datos.")
    else:
        form = ParticipantForm()

    context = {
        'form': form,
        'participants': Participant.objects.all().order_by('name'),
    }
    return render(request, 'add_participant.html', context)


@staff_member_required
def add_raffle_number(request):
    """Vista para asignar un número a un participante en un sorteo."""
    if request.method == 'POST':
        form = RaffleNumberForm(request.POST)
        if form.is_valid():
            raffle_number = form.save()
            messages.success(
                request,
                f"Número #{raffle_number.number} asignado a {raffle_number.participant.name} correctamente."
            )
            return redirect('add_raffle_number')
        else:
            messages.error(request, "No se pudo asignar el número. Verifica que no esté repetido.")
    else:
        form = RaffleNumberForm()

    return render(request, 'add_raffle_number.html', {'form': form})


@staff_member_required
def claim_daily_winner(request, winner_id):
    """Marca un premio diario como reclamado."""
    winner = get_object_or_404(DailyWinner, pk=winner_id)

    if winner.claimed:
        messages.warning(request, f"⚠️ El premio de {winner.participant.name} ya fue reclamado anteriormente.")
    else:
        winner.claimed = True
        winner.save()
        messages.success(request, f"🏆 Has marcado como reclamado el premio de {winner.participant.name}.")

    # Redirige a la página anterior o a una lista de ganadores
    return redirect(request.META.get('HTTP_REFERER', 'daily_winners_list'))