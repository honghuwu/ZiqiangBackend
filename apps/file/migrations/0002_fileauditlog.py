from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("file", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileAuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("upload", "上传文件"),
                            ("download", "下载文件"),
                            ("delete", "删除文件"),
                            ("delete_blocked", "删除被阻止"),
                            ("template_create", "创建模板"),
                            ("template_update", "更新模板"),
                            ("template_disable", "停用模板"),
                        ],
                        max_length=30,
                        verbose_name="操作类型",
                    ),
                ),
                ("template_key", models.SlugField(blank=True, default="", max_length=50, verbose_name="模板键")),
                ("ip_address", models.CharField(blank=True, default="", max_length=64, verbose_name="IP 地址")),
                ("user_agent", models.TextField(blank=True, default="", verbose_name="User-Agent")),
                ("metadata", models.JSONField(blank=True, default=dict, verbose_name="附加数据")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="file_audit_logs",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="操作人",
                    ),
                ),
                (
                    "managed_file",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="audit_logs",
                        to="file.managedfile",
                        verbose_name="关联文件",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
