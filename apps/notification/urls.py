from django.urls import path

from .views import (
    MarkAllNotificationsReadView,
    MarkNotificationReadView,
    MyNotificationDetailView,
    MyNotificationListView,
)

urlpatterns = [
    path("my/", MyNotificationListView.as_view(), name="notification-list"),
    path("my/read-all/", MarkAllNotificationsReadView.as_view(), name="notification-read-all"),
    path("my/<int:pk>/", MyNotificationDetailView.as_view(), name="notification-detail"),
    path("my/<int:pk>/read/", MarkNotificationReadView.as_view(), name="notification-read"),
]
