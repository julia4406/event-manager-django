import datetime

from django.utils import timezone
from rest_framework.exceptions import ValidationError, PermissionDenied


def validate_not_in_past(value):
    if value < timezone.now():
        raise ValidationError("Event date/time cannot be in the past.")


class EventValidators:
    @staticmethod
    def check_permissions_for_event(request, event):
        user = request.user
        if not user.is_staff and user != event.organizer:
            raise PermissionDenied("You are not the organizer of this event.")

    @staticmethod
    def check_event_date(event):
        validate_not_in_past(event.event_date)

    @staticmethod
    def already_registred(request, event):
        user = request.user
        if user in event.participants.all():
            raise ValidationError("You are already registered for this event.")

    @staticmethod
    def not_registred(request, event):
        user = request.user
        if request.user not in event.participants.all():
            raise ValidationError("You are not registered for this event.")
