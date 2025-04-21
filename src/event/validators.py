import datetime

from rest_framework.exceptions import ValidationError, PermissionDenied


class EventValidators:
    @staticmethod
    def check_permissions_for_event(request, event):
        user = request.user
        if not user.is_staff and user != event.organizer:
            raise PermissionDenied("You are not the organizer of this event.")

    @staticmethod
    def check_event_date(event):
        today = datetime.date.today()
        now = datetime.datetime.now()
        if (event.event_date < today
                or (
                        event.event_date == today
                        and event.start_of_event
                        and event.start_of_event < now
                )
                or (
                        event.event_date == today
                        and not event.start_of_event
                )
        ):
            raise ValidationError("Event already started.")

    @staticmethod
    def check_event_date_values(event_date, start_of_event=None):
        today = datetime.date.today()
        now = datetime.datetime.now()
        if (
                event_date < today
                or (
                event_date == today and start_of_event and start_of_event < now)
                or (event_date == today and start_of_event is None)
        ):
            raise ValidationError("New event couldn't be in the past.")

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
