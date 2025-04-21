from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, \
    extend_schema_view


user_participation_event_filter = {
    "parameters": [
                OpenApiParameter(
                    name="search",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Search by event title, "
                                "location or organizer username",
                ),
                OpenApiParameter(
                    name="event_format",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Filter by event format (e.g. Online, Offline)",
                ),
                OpenApiParameter(
                    name="event_date",
                    type=OpenApiTypes.DATETIME,
                    location=OpenApiParameter.QUERY,
                    description="Filter by event date (e.g.2025-04-22T18:00:00Z)",
                ),
                OpenApiParameter(
                    name="organizer",
                    type=OpenApiTypes.INT,
                    location=OpenApiParameter.QUERY,
                    description="Filter by organizer's user ID",
                ),
                OpenApiParameter(
                    name="ordering",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Sort by field "
                                "(e.g. `event_date`, `title`, or `-title`)",
                ),
    ]
}

user_organization_event_filter = {
    "parameters": [
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Search by event title, location, "
                        "or participant username",
        ),
        OpenApiParameter(
            name="event_format",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filter by event format (e.g. Online, Offline)",
        ),
        OpenApiParameter(
            name="event_date",
            type=OpenApiTypes.DATETIME,
            location=OpenApiParameter.QUERY,
            description="Filter by event date (e.g. 2025-04-22T18:00:00Z)",
        ),
        OpenApiParameter(
            name="participants",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Filter by participant user ID",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Sort by field (e.g. `event_date`,"
                        " `title`, or `-title`)",
        ),
    ]
}


def user_schema_view():
    return extend_schema_view(
        list=extend_schema(
            summary="List all users",
            description="Search users by username, email, first or last name.",
            parameters=[
                OpenApiParameter(
                    name="search",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Search by username, email, "
                                "first name or last name",
                ),
            ],
        ),
        retrieve=extend_schema(summary="Retrieve user details"),
        create=extend_schema(summary="Create a new user"),
        update=extend_schema(summary="Update a user"),
        partial_update=extend_schema(summary="Partially update a user"),
        destroy=extend_schema(summary="Delete a user"),
    )


def create_user_schema():
    return extend_schema(
        tags=["signup"],
        summary="New user registration.",
        description="Creates account for the new user."
    )


def profile_schema():
    return extend_schema(
        tags=["user profile"],
        summary="Personal user information",
        description="Retrieve and update the profile "
                    "of the currently authenticated user.",
    )


def participated_events_schema():
    return extend_schema(
            tags=["user profile"],
            summary="List events the user is attending.",
            description="Retrieves and filters events where "
                        "the current user is a participant.",
            parameters=user_participation_event_filter["parameters"]
    )


def organized_events_schema():
    return extend_schema(
            tags=["user profile"],
            summary="Retrieve events organized by current user.",
            description="Retrieves and filters events organized "
                        "by currently authenticated user.",
            parameters=user_organization_event_filter["parameters"]
    )
