from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, \
    ListAPIView
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from event.serializers import EventSerializer
from user.serializers import UserSerializer


@extend_schema(tags=["admin only: management user records"])
@extend_schema(
    tags=["admin only: management user records"],
    summary="All information about registered users",
    description="CRUD operations with profiles, "
                "search by user (username, email, first and last name).",
)
class UserListViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        "username",
        "email",
        "first_name",
        "last_name"
    ]

@extend_schema(
    tags=["signup"],
    summary="New user registration.",
    description="Creates account for the new user."
)
class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []


@extend_schema(
    tags=["user profile"],
    summary="Personal user information",
    description="Retrieve and update the profile "
                "of the currently authenticated user.",
)
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    tags=["user profile"],
    summary="List events the user is attending.",
    description="Retrieves and filters events where "
                "the current user is a participant.",
)
class ParticipatedEventsView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "title",
        "location",
        "organizer__username",
    ]
    filterset_fields = ["event_format", "event_date", "organizer"]
    ordering_fields = ["event_date", "title"]
    ordering = ["event_date"]

    def get_queryset(self):
        return self.request.user.events.all()

@extend_schema(
    tags=["user profile"],
    summary="Retrieve events organized by current user.",
    description="Retrieves and filters events organized "
                "by currently authenticated user.",
)
class OrganizedEventsView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "title",
        "location",
        "participants__username"
    ]
    filterset_fields = ["event_format", "event_date", "participants"]
    ordering_fields = ["event_date", "title"]
    ordering = ["event_date"]

    def get_queryset(self):
        return self.request.user.organized_events.all()
