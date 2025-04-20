import datetime

from django.template.context_processors import request
from rest_framework import status
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication
)
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from event.models import Event
from event.serializers import EventSerializer
from event.validators import EventValidators as validator


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # def check_permissions_for_event(self, event):
    #     user = self.request.user
    #     if not user.is_staff and user != event.organizer:
    #         raise PermissionDenied("You are not the organizer of this event.")
    #
    # def check_event_date(self, event):
    #     today = datetime.date.today()
    #     now = datetime.datetime.now()
    #     if event.event_date < today or (
    #             event.event_date == today
    #             and event.start_of_event
    #             and event.start_of_event < now):
    #         raise ValidationError("Event already started")

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_staff and "organizer" in serializer.validated_data:
            serializer.save(organizer=serializer.validated_data["organizer"])
        else:
            serializer.save(organizer=user)

    def perform_update(self, serializer):
        event = self.get_object()
        validator.check_permissions_for_event(request, event)
        serializer.save()

    def perform_destroy(self, instance):
        validator.check_permissions_for_event(request, instance)
        instance.delete()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(
        methods=["POST"],
        detail=True,
        url_path="register"
    )
    def event_registration(self, request, pk):
        event = self.get_object()
        validator.check_event_date(event)
        validator.check_registration(request, event)
        event.participants.add(request.user)
        return Response({"status": "registered"}, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="unregister"
    )
    def event_cancel_registration(self, request, pk=None):
        event = self.get_object()
        validator.check_event_date(event)
        if not event or request.user not in event.participants.all():
            return Response(
                {"detail": "Event didn't found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        event.participants.remove(request.user)
        return Response({"status": "unregistered"}, status=status.HTTP_200_OK)
