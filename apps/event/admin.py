from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "teacher",
        "event_type",
        "status",
        "start_time",
        "end_time",
        "expected_participants",
        "current_participants",
    )
    list_filter = ("status", "event_type")
    search_fields = ("title", "teacher__username", "teacher__profile__name")
