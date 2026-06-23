from django.db import models
from django.core.exceptions import ValidationError
from services.models import Service


class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Double booking protection
        existing = Booking.objects.filter(
            date=self.date,
            time=self.time,
            status__in=['Pending', 'Confirmed']
        ).exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError(
                f"This time slot ({self.time}) on {self.date} is already booked. Please choose another time."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} - {self.date} {self.time}"

    class Meta:
        ordering = ['-date', '-time']
