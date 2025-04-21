from django.db import models


class TimeSlot(models.Model):

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_holiday = models.BooleanField(default=False, blank=True)

    class Meta:
        unique_together = ('date', 'start_time', 'end_time')
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
