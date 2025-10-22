from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Raffle(models.Model):
    prize_name = models.CharField(max_length=100)
    prize_description = models.TextField(blank=True, null=True)
    prize_image = models.ImageField(upload_to='prizes/', blank=True, null=True)
    draw_date = models.DateField()
    number_winner = models.PositiveSmallIntegerField(blank=True, null=True)
    finalized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prize_name


class RaffleNumber(models.Model):
    number = models.PositiveSmallIntegerField()
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='numbers')
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='numbers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def available_numbers(self):
        """Return a list of available numbers (0–99) for the given raffle."""
        taken_numbers = RaffleNumber.objects.filter(raffle_id=self.raffle.id).values_list('number', flat=True)
        return [n for n in range(100) if n not in taken_numbers]
    
    class Meta:
        unique_together = ('number', 'raffle')

    def __str__(self):
        return f"#{self.number:02d} - {self.participant.name}"

class DailyWinner(models.Model):
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='daily_wins')
    date = models.DateField(unique=True)  # Solo un ganador por día
    claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.name} - {self.date}"