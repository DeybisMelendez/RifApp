from django import forms
from .models import Participant, RaffleNumber, Raffle

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class RaffleNumberForm(forms.ModelForm):
    class Meta:
        model = RaffleNumber
        fields = ['participant', 'raffle', 'number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Selecciona el sorteo más reciente
        latest_raffle = Raffle.objects.order_by('-created_at').first()
        if latest_raffle:
            self.fields['raffle'].initial = latest_raffle
            self.fields['raffle'].queryset = Raffle.objects.filter(id=latest_raffle.id)

            # Filtra solo los números disponibles (0–99)
            taken_numbers = RaffleNumber.objects.filter(raffle=latest_raffle).values_list('number', flat=True)
            available = [(n, f"{n:02d}") for n in range(100) if n not in taken_numbers]

            self.fields['number'] = forms.ChoiceField(choices=available, label="Número disponible")
        else:
            self.fields['number'] = forms.ChoiceField(choices=[], label="Número disponible")
