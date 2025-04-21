from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, \
    OpenApiExample, OpenApiParameter

event_filter_list_schema = {
    "parameters": [
        OpenApiParameter(
            "search",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            description="Search by event title, location, organizer "
                        "username, or participant username.",
            required=False,
        ),
        OpenApiParameter(
            "event_format",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            description="Filter by event format. Options: 'Online' or 'Offline'.",
            required=False,
        ),
        OpenApiParameter(
            "event_date",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            description="Filter events by date. Format: YYYY-MM-DD "
                        "or specific datetime (e.g. 2025-04-23T18:00:00).",
            required=False,
        ),
        OpenApiParameter(
            "organizer",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            description="Filter events by organizer's username.",
            required=False,
        ),
        OpenApiParameter(
            "participants",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            description="Filter events by participants' usernames.",
            required=False,
        ),
        OpenApiParameter(
            "ordering",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            description="Order events by field(s). Options: 'event_date', 'title'."
                        " Use commas for multiple fields.",
            required=False,
        ),
    ]
}


def event_schema_view():
    return extend_schema_view(
        list=extend_schema(
            summary="List of all events with filters",
            description="Retrieve a list of events with optional "
                        "filtering, searching and sorting.",
            parameters=event_filter_list_schema["parameters"],
        ),
        create=extend_schema(
            summary="Create a new event",
            description="Create a new event.",
        ),
        retrieve=extend_schema(
            summary="Retrieve an event",
            description="Retrieve a specific event by its ID.",
        ),
        update=extend_schema(
            summary="Update an event",
            description="Update an event's details.",
        ),
        partial_update=extend_schema(
            summary="Partially update an event information",
            description="Partially update an event's details.",
        ),
        destroy=extend_schema(
            summary="Delete an event",
            description="Delete a specific event.",
        ),
        event_registration=extend_schema(
            summary="Registration on event",
            description="Register current user on specific event.",
        ),
        event_cancel_registration = extend_schema(
        summary="Cancelling registration on event",
        description="Cancel registration of current user for specific event.",
        )
    )
