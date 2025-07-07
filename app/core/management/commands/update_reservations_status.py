from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Reservation


class Command(BaseCommand):
    help = 'Atualiza o status das reservas cujo horário já passou para "concluída"'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        queryset = Reservation.objects.filter(
            status="confirmada", time_slot__end_time__lt=now
        )

        updated_count = queryset.update(status="concluída")

        self.stdout.write(
            self.style.SUCCESS(
                f'{updated_count} reservas atualizadas para "concluída".'
            )
        )
