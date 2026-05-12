from django.apps import AppConfig


class ManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.management"
    verbose_name = "管理员管理"
