from django.urls import path

from .views import (
    CloseEventView,
    PublicEventDetailView,
    PublicEventListView,
    PublishEventView,
    StudentApplicationDetailView,
    StudentApplicationListCreateView,
    TeacherApplicationApproveView,
    TeacherApplicationListView,
    TeacherApplicationRejectView,
    TeacherEventDetailView,
    TeacherEventListCreateView,
)

urlpatterns = [
    path("events/", PublicEventListView.as_view(), name="event-list"),
    path("events/<int:pk>/", PublicEventDetailView.as_view(), name="event-detail"),
    path("events/<int:event_pk>/apply/", StudentApplicationListCreateView.as_view(), name="event-apply"),
    path("my-applications/", StudentApplicationListCreateView.as_view(), name="my-application-list"),
    path("my-applications/<int:pk>/", StudentApplicationDetailView.as_view(), name="my-application-detail"),
    path("teacher/events/", TeacherEventListCreateView.as_view(), name="teacher-event-list"),
    path("teacher/events/<int:pk>/", TeacherEventDetailView.as_view(), name="teacher-event-detail"),
    path("teacher/events/<int:pk>/publish/", PublishEventView.as_view(), name="teacher-event-publish"),
    path("teacher/events/<int:pk>/close/", CloseEventView.as_view(), name="teacher-event-close"),
    path("teacher/applications/", TeacherApplicationListView.as_view(), name="teacher-application-list"),
    path(
        "teacher/applications/<int:pk>/approve/",
        TeacherApplicationApproveView.as_view(),
        name="teacher-application-approve",
    ),
    path(
        "teacher/applications/<int:pk>/reject/",
        TeacherApplicationRejectView.as_view(),
        name="teacher-application-reject",
    ),
]
