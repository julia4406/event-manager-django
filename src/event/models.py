from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


class Event(models.Model):
    class Format(models.TextChoices):
        ONLINE = "Online"
        OFFLINE = "Offline"

    title = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    start_of_event = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=63, blank=True, null=True)
    event_format = models.CharField(max_length=15, choices=Format)
    organizer = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events"
    )
    participants = models.ManyToManyField(
        AUTH_USER_MODEL,
        through="EventUser",
        related_name="events"
    )

    def __str__(self):
        if self.start_of_event:
            return f"{self.title} on {self.event_date} at {self.start_of_event}"
        return f"{self.title} on {self.event_date}"


class EventUser(models.Model):
    class RegistrationStatus(models.TextChoices):
        REGISTERED = "Registered"
        CANCELLED = "Cancelled"

    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    participant = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15,
        choices=RegistrationStatus,
        default=RegistrationStatus.REGISTERED
    )
