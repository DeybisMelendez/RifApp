from django.contrib import admin
from .models import Participant, Raffle, RaffleNumber


class RaffleNumberInline(admin.TabularInline):
    """Permite gestionar los números de la rifa directamente desde la vista de la rifa."""
    model = RaffleNumber
    extra = 5  # número de filas vacías para agregar rápidamente
    fields = ('number', 'participant', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['participant']
    ordering = ['number']


@admin.register(Raffle)
class RaffleAdmin(admin.ModelAdmin):
    list_display = ('prize_name', 'draw_date', 'finalized', 'created_at', 'total_numbers')
    list_filter = ('finalized', 'draw_date',)
    search_fields = ('prize_name', 'prize_description',)
    date_hierarchy = 'draw_date'
    inlines = [RaffleNumberInline]
    readonly_fields = ('created_at',)
    ordering = ['-created_at']

    def total_numbers(self, obj):
        """Muestra cuántos números han sido vendidos/asignados en la rifa."""
        return obj.numbers.count()
    total_numbers.short_description = "Números asignados"


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_tickets', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    ordering = ['name']

    def total_tickets(self, obj):
        return obj.numbers.count()
    total_tickets.short_description = "Total de números"


@admin.register(RaffleNumber)
class RaffleNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'raffle', 'participant', 'created_at')
    list_filter = ('raffle',)
    search_fields = ('participant__name', 'raffle__prize_name')
    readonly_fields = ('created_at',)
    ordering = ['raffle', 'number']
    autocomplete_fields = ['participant', 'raffle']
