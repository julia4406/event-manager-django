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
    organizer = models.CharField(max_length=63)

    def __str__(self):
        if self.start_of_event:
            return f"{self.title} on {self.event_date} at {self.start_of_event}"
        return f"{self.title} on {self.event_date}"
