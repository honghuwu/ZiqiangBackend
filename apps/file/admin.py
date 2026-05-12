from django.contrib import admin

from .models import FileAuditLog, FileTemplate, ManagedFile


@admin.register(ManagedFile)
class ManagedFileAdmin(admin.ModelAdmin):
    list_display = ("id", "original_name", "category", "uploaded_by", "file_size", "created_at")
    list_filter = ("category",)
    search_fields = ("original_name", "description", "uploaded_by__username")


@admin.register(FileTemplate)
class FileTemplateAdmin(admin.ModelAdmin):
    list_display = ("key", "name", "file", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("key", "name")


@admin.register(FileAuditLog)
class FileAuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "actor", "managed_file", "template_key", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("actor__username", "template_key", "managed_file__original_name")
    readonly_fields = ("actor", "action", "managed_file", "template_key", "ip_address", "user_agent", "metadata", "created_at")
