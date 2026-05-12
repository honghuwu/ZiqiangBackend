from django.urls import path

from .views import (
    AdminFileTemplateDetailView,
    AdminFileTemplateListCreateView,
    FileTemplateDetailView,
    FileTemplateListView,
    ManagedFileDownloadView,
    ManagedFileDetailView,
    ManagedFileListView,
    ManagedFileUploadView,
)

urlpatterns = [
    path("uploads/", ManagedFileUploadView.as_view(), name="file-upload"),
    path("my-files/", ManagedFileListView.as_view(), name="file-list"),
    path("uploads/<uuid:id>/", ManagedFileDetailView.as_view(), name="file-detail"),
    path("uploads/<uuid:id>/download/", ManagedFileDownloadView.as_view(), name="file-download"),
    path("templates/", FileTemplateListView.as_view(), name="file-template-list"),
    path("templates/<slug:key>/", FileTemplateDetailView.as_view(), name="file-template-detail"),
    path("admin/templates/", AdminFileTemplateListCreateView.as_view(), name="admin-file-template-list"),
    path(
        "admin/templates/<slug:key>/",
        AdminFileTemplateDetailView.as_view(),
        name="admin-file-template-detail",
    ),
]
