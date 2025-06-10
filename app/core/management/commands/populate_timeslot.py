from django.core.management.base import BaseCommand
from core.models import TimeSlot
from datetime import datetime, timedelta, time


class Command(BaseCommand):
    help = "Popula os TimeSlots no banco de dados para os anos de 2025 e 2026."

    def handle(self, *args, **options):
        start_date = datetime(2025, 6, 10)
        end_date = datetime(2026, 6, 10)
        delta = timedelta(days=1)

        holidays = get_national_holidays(2025) | get_national_holidays(2026)

        while start_date <= end_date:
            is_sunday = start_date.weekday() == 6
            is_holiday = start_date.date() in holidays

            if is_sunday or is_holiday:
                day_start = time(5, 0)
                day_end = time(13, 0)
            else:
                day_start = time(5, 0)
                day_end = time(22, 0)

            # Gerar slots de 1 hora dentro do intervalo
            current_start = datetime.combine(start_date.date(), day_start)
            day_end_dt = datetime.combine(start_date.date(), day_end)

            while current_start < day_end_dt:
                current_end = current_start + timedelta(hours=1)
                # Garante que o end_time não ultrapasse o horário final do dia
                if current_end > day_end_dt:
                    current_end = day_end_dt

                TimeSlot.objects.update_or_create(
                    date=start_date.date(),
                    start_time=current_start.time(),
                    end_time=current_end.time(),
                    defaults={
                        "is_holiday": is_holiday,
                        "is_available": True,
                    },
                )
                current_start = current_end

            start_date += delta


def get_national_holidays(year):
    holidays = [
        datetime(year, 1, 1),
        datetime(year, 4, 21),
        datetime(year, 5, 1),
        datetime(year, 9, 7),
        datetime(year, 10, 12),
        datetime(year, 11, 2),
        datetime(year, 11, 15),
        datetime(year, 12, 25),
    ]
    easter = calculate_easter(year)
    holidays.append(easter - timedelta(days=2))  # Sexta-feira Santa
    holidays.append(easter + timedelta(days=60))  # Corpus Christi
    holidays.append(easter)  # Páscoa
    holidays.append(easter - timedelta(days=47))  # Carnaval (terça-feira)
    holidays.append(easter - timedelta(days=48))  # Carnaval (segunda-feira)
    return set([h.date() for h in holidays])


def calculate_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day)
