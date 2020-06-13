from datetime import datetime

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField()

    def availability(self):
        present = datetime.now().date()
        reservations = Reservation.objects.filter(room=self.id)
        reservation_dates = []
        for reservation in reservations:
            reservation_dates.append(reservation.date)
        if present in reservation_dates:
            return "Not Available"
        return "Available"

class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('date', 'room')

