from django.core.management.base import BaseCommand
from core.models import TimeSlot
from datetime import datetime, timedelta, time


class Command(BaseCommand):
    help = "Popula os TimeSlots no banco de dados para os anos de 2025 e 2026."

    def handle(self, *args, **options):
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2026, 12, 31)
        delta = timedelta(days=1)

        # Gera os feriados para ambos os anos e une os conjuntos
        holidays = get_national_holidays(2025) | get_national_holidays(2026)

        while start_date <= end_date:
            is_sunday = start_date.weekday() == 6
            is_holiday = start_date.date() in holidays

            if is_sunday or is_holiday:
                start_time = time(5, 0)
                end_time = time(13, 0)
            else:
                start_time = time(5, 0)
                end_time = time(22, 0)

            TimeSlot.objects.update_or_create(
                date=start_date.date(),
                defaults={"start_time": start_time, "end_time": end_time, "is_holiday": is_holiday},
            )

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
    print( set([h.date() for h in holidays]) )
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
