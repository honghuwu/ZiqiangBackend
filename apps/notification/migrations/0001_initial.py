from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("event_application_submitted", "项目申请提交"),
                            ("event_application_approved", "项目申请通过"),
                            ("event_application_rejected", "项目申请拒绝"),
                        ],
                        max_length=50,
                        verbose_name="通知类型",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="标题")),
                ("content", models.TextField(verbose_name="内容")),
                ("is_read", models.BooleanField(default=False, verbose_name="是否已读")),
                ("read_at", models.DateTimeField(blank=True, null=True, verbose_name="已读时间")),
                ("metadata", models.JSONField(blank=True, default=dict, verbose_name="附加数据")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="接收人",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
