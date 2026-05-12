from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    AdminApplicationApproveView,
    AdminApplicationListView,
    AdminApplicationRejectView,
    AdminCsrfTokenView,
    AdminDashboardView,
    AdminEventCloseView,
    AdminEventCreateView,
    AdminEventDetailView,
    AdminEventListView,
    AdminEventPublishView,
    AdminEventUpdateView,
    AdminFileDeleteView,
    AdminFileListView,
    AdminLoginView,
    AdminLogoutView,
    AdminUserCreateView,
    AdminUserDeleteView,
    AdminUserDetailView,
    AdminUserListView,
    AdminUserUpdateView,
)

urlpatterns = [
    path("login/", csrf_exempt(AdminLoginView.as_view()), name="admin-login"),
    path("logout/", AdminLogoutView.as_view(), name="admin-logout"),
    path("csrf/", AdminCsrfTokenView.as_view(), name="admin-csrf"),

    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),

    path("users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),
    path("users/<int:pk>/update/", AdminUserUpdateView.as_view(), name="admin-user-update"),
    path("users/<int:pk>/delete/", AdminUserDeleteView.as_view(), name="admin-user-delete"),
    path("users/create/", AdminUserCreateView.as_view(), name="admin-user-create"),

    path("events/", AdminEventListView.as_view(), name="admin-event-list"),
    path("events/create/", AdminEventCreateView.as_view(), name="admin-event-create"),
    path("events/<int:pk>/", AdminEventDetailView.as_view(), name="admin-event-detail"),
    path("events/<int:pk>/update/", AdminEventUpdateView.as_view(), name="admin-event-update"),
    path("events/<int:pk>/publish/", AdminEventPublishView.as_view(), name="admin-event-publish"),
    path("events/<int:pk>/close/", AdminEventCloseView.as_view(), name="admin-event-close"),

    path("applications/", AdminApplicationListView.as_view(), name="admin-application-list"),
    path(
        "applications/<int:pk>/approve/",
        AdminApplicationApproveView.as_view(),
        name="admin-application-approve",
    ),
    path(
        "applications/<int:pk>/reject/",
        AdminApplicationRejectView.as_view(),
        name="admin-application-reject",
    ),

    path("files/", AdminFileListView.as_view(), name="admin-file-list"),
    path("files/<uuid:pk>/", AdminFileDeleteView.as_view(), name="admin-file-delete"),
]
